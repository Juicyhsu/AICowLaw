"""
批次匯入現有筆記到 Pinecone 向量資料庫
用於將 Airtable 中的舊筆記加入 Pinecone，啟用智慧搜尋功能
"""
# -*- coding: utf-8 -*-
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from data_manager import DataManager
from ai_core import AICore
import time

def import_notes_to_pinecone():
    """將所有 Airtable 筆記匯入 Pinecone"""
    
    print("=" * 60)
    print("📦 批次匯入筆記到 Pinecone 向量資料庫")
    print("=" * 60)
    
    # 初始化
    data_manager = DataManager()
    ai_core = AICore()
    
    # 取得所有使用者
    users = ["九水", "使用者A", "使用者B", "使用者C", "使用者D"]
    
    total_notes = 0
    success_count = 0
    fail_count = 0
    skip_count = 0
    
    for user_id in users:
        print(f"\n🔍 處理使用者：{user_id}")
        
        # 取得該使用者的所有筆記
        notes = data_manager.get_all_notes(user_id)
        
        if not notes:
            print(f"  ℹ️ {user_id} 沒有筆記")
            continue
        
        print(f"  📝 找到 {len(notes)} 則筆記")
        
        for i, note in enumerate(notes, 1):
            total_notes += 1
            note_id = note.get('id')
            title = note.get('title', '無標題')
            content = note.get('content', '')
            
            # 檢查是否有內容
            if not content or len(content.strip()) < 10:
                print(f"  ⏭️ [{i}/{len(notes)}] 跳過：{title}（內容太短）")
                skip_count += 1
                continue
            
            try:
                # 加入 Pinecone
                ai_core.add_to_knowledge_base(
                    content=content,
                    metadata={
                        'note_id': note_id,
                        'user_id': user_id,
                        'title': title,
                        'category': note.get('category', '一般'),
                        'tags': note.get('tags', []),
                        'difficulty': note.get('difficulty', '中等'),
                        'type': 'note'
                    }
                )
                
                print(f"  ✅ [{i}/{len(notes)}] 已匯入：{title}")
                success_count += 1
                
                # 避免 API 限制，稍微延遲
                time.sleep(0.1)
                
            except Exception as e:
                print(f"  ❌ [{i}/{len(notes)}] 失敗：{title}")
                print(f"     錯誤：{e}")
                fail_count += 1
    
    # 顯示統計
    print("\n" + "=" * 60)
    print("📊 匯入統計")
    print("=" * 60)
    print(f"總筆記數：{total_notes}")
    print(f"✅ 成功匯入：{success_count}")
    print(f"❌ 匯入失敗：{fail_count}")
    print(f"⏭️ 跳過（內容太短）：{skip_count}")
    print("=" * 60)
    
    if success_count > 0:
        print("\n🎉 匯入完成！現在可以使用智慧搜尋功能了！")
    else:
        print("\n⚠️ 沒有成功匯入任何筆記，請檢查錯誤訊息")

if __name__ == "__main__":
    try:
        import_notes_to_pinecone()
    except KeyboardInterrupt:
        print("\n\n⚠️ 使用者中斷匯入")
    except Exception as e:
        print(f"\n\n❌ 發生錯誤：{e}")
        import traceback
        traceback.print_exc()
