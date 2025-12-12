"""
法律考試輔助系統 - AI 核心模組（完整版 + 風格支援 + 視覺化）
處理 Gemini API、Pinecone 向量搜尋、RAG 問答、心智圖生成
"""

import google.generativeai as genai
from pinecone import Pinecone, ServerlessSpec
from config import Config
from ai_cache import AICache
import time
import json
import re
from typing import List, Dict, Optional

class AICore:
    """AI 核心處理類別"""
    
    def __init__(self):
        """初始化 AI 服務"""
        try:
            # 配置 Gemini
            genai.configure(api_key=Config.GEMINI_API_KEY)
            
            # 初始化模型
            self.model = genai.GenerativeModel(Config.GEMINI_MODEL)
            self.embedding_model = Config.EMBEDDING_MODEL
            
            # 初始化 Pinecone
            self.pc = Pinecone(api_key=Config.PINECONE_API_KEY)
            self.index = self._init_pinecone_index()
            
            # 初始化 AI 快取
            self.cache = AICache(cache_file="ai_cache.json", max_age_hours=24)
            
            print("✅ AI 服務初始化成功")
            
        except Exception as e:
            print(f"❌ AI 初始化失敗: {e}")
            raise
    
    def _init_pinecone_index(self):
        """初始化 Pinecone 索引"""
        index_name = Config.PINECONE_INDEX_NAME
        
        # 檢查索引是否存在
        existing_indexes = [idx['name'] for idx in self.pc.list_indexes()]
        
        if index_name not in existing_indexes:
            print(f"📦 建立新的 Pinecone 索引: {index_name}")
            self.pc.create_index(
                name=index_name,
                dimension=Config.EMBEDDING_DIMENSION,
                metric='cosine',
                spec=ServerlessSpec(
                    cloud='aws',
                    region='us-east-1'
                )
            )
            # 等待索引準備就緒
            print("⏳ 等待索引初始化...")
            time.sleep(10)
        
        # 連接到索引並返回
        index = self.pc.Index(index_name)
        print(f"✅ Pinecone 索引已連接: {index_name}")
        return index
    
    def generate_embedding(self, text: str) -> List[float]:
        """生成文字嵌入向量"""
        try:
            result = genai.embed_content(
                model=Config.EMBEDDING_MODEL,
                content=text,
                task_type="retrieval_document"
            )
            return result['embedding']
        except Exception as e:
            print(f"❌ 嵌入生成錯誤: {e}")
            return [0.0] * Config.EMBEDDING_DIMENSION
    
    def add_to_knowledge_base(self, content: str, metadata: Dict) -> bool:
        """新增內容到知識庫"""
        try:
            embedding = self.generate_embedding(content)
            doc_id = f"{metadata.get('type', 'doc')}_{int(time.time() * 1000)}"
            
            self.index.upsert(
                vectors=[{
                    'id': doc_id,
                    'values': embedding,
                    'metadata': {
                        'content': content[:1000],
                        'full_content': content,
                        **metadata
                    }
                }]
            )
            
            print(f"✅ 已加入知識庫: {metadata.get('title', 'Untitled')}")
            return True
            
        except Exception as e:
            print(f"❌ 加入知識庫失敗: {e}")
            return False
    
    def delete_from_knowledge_base(self, note_id: str) -> bool:
        """從知識庫刪除內容"""
        try:
            self.index.delete(ids=[note_id])
            print(f"✅ 已從知識庫刪除: {note_id}")
            return True
        except Exception as e:
            print(f"❌ 從知識庫刪除失敗: {e}")
            return False
    
    def search_knowledge_base(self, query: str, top_k: int = None, 
                             category: str = None) -> List[Dict]:
        """搜尋知識庫"""
        if top_k is None:
            top_k = Config.MAX_SEARCH_RESULTS
        
        try:
            query_embedding = self.generate_embedding(query)
            filter_dict = {'category': category} if category else None
            
            results = self.index.query(
                vector=query_embedding,
                top_k=top_k * 2,
                include_metadata=True,
                filter=filter_dict
            )
            
            # 除錯：顯示所有結果的分數
            print(f"🔍 Pinecone 返回 {len(results.get('matches', []))} 個結果")
            for i, match in enumerate(results.get('matches', [])[:5]):
                print(f"  結果 {i+1}: 分數 {match['score']:.3f}")
            
            filtered_results = []
            for match in results['matches']:
                # 閾值 0.6：只顯示高度相關的結果
                if match['score'] >= 0.6:
                    filtered_results.append({
                        'score': match['score'],
                        'content': match['metadata'].get('full_content', 
                                                        match['metadata'].get('content', '')),
                        'metadata': match['metadata']
                    })
            
            filtered_results = filtered_results[:top_k]
            print(f"✅ 過濾後找到 {len(filtered_results)} 個相關結果（閾值 >= 0.6）")
            return filtered_results
            
        except Exception as e:
            print(f"❌ 搜尋失敗: {e}")
            import traceback
            traceback.print_exc()
            return []
    
    def generate_ai_notes(self, content: str, note_type: str = "重點整理", 
                         style_instruction: str = "") -> str:
        """使用 AI 生成筆記（支援自訂風格）"""
        
        base_prompts = {
            "重點整理": f"""請將以下法律內容整理成筆記。

風格要求：{style_instruction}

原始內容：
{content}

**重要指示**：
1. 直接輸出筆記內容，不要有任何開場白（例如：「好的」、「以下是」、「已為您整理」等）
2. 不要有結尾祝福或鼓勵的話
3. 不要說明你做了什麼，直接給出結果
4. 用繁體中文
5. 立即從筆記標題或內容開始""",

            "考點分析": f"""請分析以下內容的重要考點。

風格要求：{style_instruction}

原始內容：
{content}

**重要指示**：
1. 直接輸出考點分析內容，不要有任何開場白（例如：「好的」、「以下是」、「已為您整理」等）
2. 不要有結尾祝福或鼓勵的話
3. 不要說明你做了什麼，直接給出結果
4. 用繁體中文
5. 立即從考點內容開始""",

            "案例解析": f"""請針對以下內容提供案例解析。

風格要求：{style_instruction}

原始內容：
{content}

**重要指示**：
1. 直接輸出案例解析內容，不要有任何開場白（例如：「好的」、「以下是」、「已為您整理」等）
2. 不要有結尾祝福或鼓勵的話
3. 不要說明你做了什麼，直接給出結果
4. 用繁體中文
5. 立即從案例內容開始"""
        }
        
        max_retries = 3
        retry_delay = 2
        
        for attempt in range(max_retries):
            try:
                prompt = base_prompts.get(note_type, base_prompts["重點整理"])
                print(f"🤖 正在生成{note_type}... (嘗試 {attempt + 1}/{max_retries})")
                
                # 生成內容（Gemini API 不支援 request_options）
                response = self.model.generate_content(prompt)
                
                print(f"✅ {note_type}生成完成")
                
                # 後處理：移除常見的開場白模式
                result = response.text.strip()
                
                # 移除常見的開場白句子（包含 OCR 專用）
                preamble_patterns = [
                    r'^好的[，,。！!]*',
                    r'^以下是.*?[：:]\s*',
                    r'^已為您整理.*?[：:]\s*',
                    r'^這份.*?筆記.*?如下.*?[：:]\s*',
                    r'^根據.*?內容.*?[：:]\s*',
                    r'^.*?整理如下.*?[：:]\s*',
                    r'^.*?已整理.*?[：:]\s*',
                    r'^讓我.*?[：:]\s*',
                    r'^我將.*?[：:]\s*',
                    r'^以下.*?Markdown.*?[：:]\s*',
                    # OCR 專用模式
                    r'^以下是根據.*?OCR.*?辨識.*?[：:，,。]*\s*',
                    r'^根據.*?OCR.*?文字.*?[：:，,。]*\s*',
                    r'^以下是.*?OCR.*?內容.*?[：:，,。]*\s*',
                    r'^.*?整理而成的.*?內容.*?[：:，,。]*\s*',
                    r'^.*?通順.*?完整.*?格式化.*?[：:，,。]*\s*',
                ]
                
                for pattern in preamble_patterns:
                    result = re.sub(pattern, '', result, flags=re.MULTILINE)
                
                # 移除開頭的空行
                result = result.lstrip('\n')
                
                return result
                
            except Exception as e:
                error_str = str(e)
                if "504" in error_str or "timeout" in error_str.lower():
                    if attempt < max_retries - 1:
                        print(f"⚠️ 請求超時，{retry_delay}秒後重試...")
                        time.sleep(retry_delay)
                        retry_delay *= 2  # 指數退避
                        continue
                    else:
                        return f"生成筆記時發生錯誤：請求超時。請嘗試：\n1. 減少輸入內容長度\n2. 稍後再試\n3. 檢查網路連線"
                else:
                    error_msg = f"生成筆記時發生錯誤: {e}"
                    print(f"❌ {error_msg}")
                    return error_msg
    
    def answer_question_with_rag(self, question: str, 
                                 context_results: List[Dict] = None) -> str:
        """使用 RAG 回答問題"""
        if context_results is None:
            context_results = self.search_knowledge_base(question, top_k=3)
        
        if context_results:
            context = "\n\n".join([
                f"【參考資料 {i+1}】（相關度: {r['score']:.1%})\n"
                f"標題: {r['metadata'].get('title', '無標題')}\n"
                f"內容: {r['content']}"
                for i, r in enumerate(context_results)
            ])
        else:
            context = "（知識庫中暫無相關資料）"
        
        prompt = f"""你是一位專業的法律考試輔導老師。請根據知識庫內容回答學生的問題。

【知識庫參考資料】
{context}

【學生問題】
{question}

請以專業但易懂的方式回答，包含：
1. 直接回答問題的核心
2. 引用相關法條（如果有）
3. 說明在實務上的應用
4. 補充注意事項

如果知識庫內容不足，請先說明「知識庫中相關資料有限」，然後基於一般法律原則提供建議。
只輸出回答內容，不要有開場白或結尾祝福。用繁體中文。"""
        
        try:
            print(f"🤖 正在思考答案...")
            response = self.model.generate_content(prompt)
            print(f"✅ 回答完成")
            return response.text
            
        except Exception as e:
            error_msg = f"回答問題時發生錯誤: {e}"
            print(f"❌ {error_msg}")
            return error_msg
    
    def generate_quiz_question(self, content: str = None, category: str = None) -> Dict:
        """生成法律爭點選擇題（JSON 格式）"""
        
        source_content = ""
        if content:
            source_content = f"基於以下筆記內容出題：\n{content}"
        else:
            source_content = f"請出一題關於「{category if category else '法律'}」的爭點選擇題。"

        prompt = f"""你是一個法律出題老師。請{source_content}

請生成一個單選題，格式必須是合法的 JSON，包含以下欄位：
1. question: 題目敘述
2. options: 一個包含 4 個選項字串的陣列 (不需要 A, B, C, D 前綴)
3. answer_index: 正確答案的索引 (0-3)
4. explanation: 詳細解析

範例格式：
{{
  "question": "關於...下列何者正確？",
  "options": ["選項一", "選項二", "選項三", "選項四"],
  "answer_index": 1,
  "explanation": "因為..."
}}

請只輸出 JSON，不要有 Markdown code block 標記或其他文字。用繁體中文。"""

        try:
            print(f"🤖 正在生成題目...")
            response = self.model.generate_content(prompt)
            text = response.text.strip()
            
            # 嘗試解析 JSON
            match = re.search(r'\{.*\}', text, re.DOTALL)
            if match:
                json_str = match.group(0)
                quiz_data = json.loads(json_str)
                print(f"✅ 題目生成完成")
                return quiz_data
            else:
                print(f"⚠️ 無法解析 JSON，原始回應：{text}")
                return {
                    "question": "題目生成失敗，請重試",
                    "options": ["錯誤", "錯誤", "錯誤", "錯誤"],
                    "answer_index": 0,
                    "explanation": f"無法解析 AI 回應: {text}"
                }
                
        except Exception as e:
            error_msg = f"生成題目錯誤: {e}"
            print(f"❌ {error_msg}")
            return {
                "question": "發生錯誤",
                "options": ["錯誤", "錯誤", "錯誤", "錯誤"],
                "answer_index": 0,
                "explanation": error_msg
            }

    def chat_with_ai(self, message: str, chat_history: List[Dict] = None,
                    mode: str = "reference") -> str:
        """與 AI 對話"""
        if chat_history is None:
            chat_history = []
        
        conversation_context = "\n".join([
            f"{'學生' if msg['role'] == 'user' else 'AI老師'}: {msg['content']}"
            for msg in chat_history[-5:]
        ])
        
        mode_prompts = {
            "reference": """你是一位專業的法律參考書助手。學生會問你各種法律問題，請：
- 提供清晰、準確的答案
- 引用相關法條
- 用易懂的方式解釋複雜概念
- 保持專業但友善的語氣
- 只輸出回答內容，不要有開場白或結尾祝福""",

            "socratic": """你是一位使用蘇格拉底問答法的法律老師。請：
- 用提問引導學生思考
- 不要直接給答案，而是引導學生自己找到答案
- 循序漸進地深入探討
- 讚賞學生的思考過程
- 只輸出回答內容，不要有開場白或結尾祝福""",

            "game": """你是一位出題測驗的法律老師。請：
- 出具體的法律爭點選擇題或情境題
- 提供明確的選項（A) B) C) D)）
- 學生回答後給予詳細解析
- 保持遊戲化、有趣的氛圍
- 如果學生說「開始」，就出第一題
- 只輸出題目或解析內容，不要有開場白或結尾祝福"""
        }
        
        mode_instruction = mode_prompts.get(mode, mode_prompts["reference"])
        
        prompt = f"""{mode_instruction}

【對話記錄】
{conversation_context if conversation_context else '（這是對話的開始）'}

【學生最新訊息】
{message}

請回應學生。用繁體中文。"""
        
        try:
            print(f"🤖 {mode} 模式回應中...")
            response = self.model.generate_content(prompt)
            print(f"✅ 回應完成")
            return response.text
            
        except Exception as e:
            error_msg = f"對話時發生錯誤: {e}"
            print(f"❌ {error_msg}")
            return error_msg
    
    def generate_mind_map(self, content: str) -> str:
        """生成 Mermaid 心智圖"""
        prompt = f"""請將以下筆記內容轉換成 Mermaid 心智圖格式。

內容：
{content}

嚴格要求：
1. 使用 mindmap 語法
2. 最多3層結構
3. **所有文字必須使用繁體中文**，絕對不可以有英文、德文或其他語言
4. 節點名稱要簡短（每個節點不超過10個字）
5. 避免使用特殊符號，只用中文、數字、括號
6. 只輸出 Mermaid 程式碼，不要有任何其他文字或說明
7. 不要使用 ``` 符號包裹

正確格式範例：
mindmap
  root((侵權行為))
    構成要件
      故意或過失
      不法行為
      損害發生
    法律效果
      損害賠償
      回復原狀

請生成（只輸出程式碼，不要有任何解釋）："""
        
        try:
            response = self.model.generate_content(prompt)
            result = response.text.strip()
            
            # 移除可能的 markdown code block 標記
            if "```" in result:
                parts = result.split("```")
                if len(parts) >= 3:
                    result = parts[1]
                elif len(parts) == 2:
                    result = parts[1]
            
            # 移除語言標記
            if result.startswith("mermaid"):
                result = result[7:].strip()
            elif result.startswith("mindmap"):
                pass  # 保留 mindmap
            
            # 確保以 mindmap 開頭
            if not result.strip().startswith("mindmap"):
                result = "mindmap\n" + result
            
            return result.strip()
        except Exception as e:
            return f"mindmap\n  root((錯誤))\n    {str(e)}"
    
    def generate_legal_system_diagram(self, content: str) -> str:
        """生成法律體系架構圖（直列版本 TB）"""
        prompt = f"""請將以下法律內容轉換成體系架構圖（Mermaid flowchart）。

內容：
{content}

嚴格要求：
1. 使用 flowchart TB 語法（Top to Bottom，由上而下直列排列）
2. **所有文字必須使用繁體中文**，絕對不可以有英文、德文或其他語言
3. 節點 ID 使用簡單的英文字母（A, B, C...）
4. 節點標籤使用繁體中文，用方括號包裹，例如：A[侵權行為]
5. 連接線使用 --> 符號
6. 節點名稱要簡短（每個不超過8個字）
7. 只輸出 Mermaid 程式碼，不要有任何其他文字或說明
8. 不要使用 ``` 符號包裹

正確格式範例：
flowchart TB
    A[侵權行為] --> B[故意侵權]
    A --> C[過失侵權]
    B --> D[損害賠償]
    C --> D

請生成（只輸出程式碼，不要有任何解釋）："""
        
        try:
            response = self.model.generate_content(prompt)
            result = response.text.strip()
            
            # 移除可能的 markdown code block 標記
            if "```" in result:
                parts = result.split("```")
                if len(parts) >= 3:
                    result = parts[1]
                elif len(parts) == 2:
                    result = parts[1]
            
            # 移除語言標記
            if result.startswith("mermaid"):
                result = result[7:].strip()
            elif result.startswith("flowchart"):
                pass  # 保留 flowchart
            
            # 確保使用 TB 方向（直列）
            if not result.strip().startswith("flowchart TB"):
                result = result.replace("flowchart LR", "flowchart TB")
                result = result.replace("flowchart TD", "flowchart TB")
                if not result.strip().startswith("flowchart"):
                    result = "flowchart TB\n" + result
            
            return result.strip()
        except Exception as e:
            return f"flowchart TB\n    A[錯誤: {str(e)}]"
    
    def get_index_stats(self) -> Dict:
        """取得知識庫統計資訊"""
        try:
            stats = self.index.describe_index_stats()
            return {
                'total_vectors': stats.get('total_vector_count', 0),
                'dimension': stats.get('dimension', Config.EMBEDDING_DIMENSION),
                'index_fullness': stats.get('index_fullness', 0)
            }
        except Exception as e:
            print(f"❌ 取得統計失敗: {e}")
            return {
                'total_vectors': 0,
                'dimension': Config.EMBEDDING_DIMENSION,
                'index_fullness': 0
            }