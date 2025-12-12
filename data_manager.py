"""
資料管理模組 - Airtable 雲端版（多裝置同步 + 多使用者支援）
"""

from pyairtable import Api
from datetime import datetime, timedelta
from config import Config
import math

class DataManager:
    def __init__(self):
        self.api = Api(Config.AIRTABLE_API_KEY)
        self.table = self.api.table(Config.AIRTABLE_BASE_ID, Config.AIRTABLE_TABLE_NAME)
        print("✅ Airtable 連接成功")
    
    def save_note(self, user_id: str, title: str, content: str, category: str = "一般", 
                  tags: list = None, difficulty: str = "中等", test_mode: bool = False) -> dict:
        """儲存筆記到 Airtable 並加入 Pinecone 向量資料庫"""
        # 測試模式：立即複習 / 正式模式：明天複習
        if test_mode:
            next_review_time = datetime.now() - timedelta(minutes=1)  # 1分鐘前（確保立即出現）
            review_msg = "立即開始複習（測試模式）"
        else:
            next_review_time = datetime.now() + timedelta(days=1)  # 明天複習
            review_msg = "明天開始複習"
        
        note = {
            'user_id': user_id,
            'title': title,
            'content': content,
            'category': category,
            'tags': ','.join(tags) if tags else '',
            'difficulty': difficulty,
            'review_count': 0,
            'ease_factor': Config.EASE_FACTOR_DEFAULT,
            'interval': 0,
            'next_review': next_review_time.isoformat(),
            'created_at': datetime.now().isoformat()  # 加入建立時間
        }
        result = self.table.create(note)
        
        # 加入 Pinecone 向量資料庫（用於智慧搜尋）
        try:
            from ai_core import AICore
            ai_core = AICore()
            ai_core.add_to_knowledge_base(
                content=content,
                metadata={
                    'note_id': result['id'],
                    'user_id': user_id,
                    'title': title,
                    'category': category,
                    'tags': tags if tags else [],
                    'difficulty': difficulty,
                    'type': 'note'
                }
            )
            print(f"✅ 筆記已加入 Pinecone 向量資料庫")
        except Exception as e:
            print(f"⚠️ 加入 Pinecone 失敗（不影響筆記儲存）: {e}")
        
        return result['fields']
    
    def get_all_notes(self, user_id: str) -> list:
        """取得該使用者的所有筆記"""
        formula = f"{{user_id}}='{user_id}'"
        records = self.table.all(formula=formula)
        notes = []
        for r in records:
            f = r['fields']
            notes.append({
                'id': r['id'],
                'user_id': f.get('user_id', ''),
                'title': f.get('title', ''),
                'content': f.get('content', ''),
                'category': f.get('category', ''),
                'tags': f.get('tags', '').split(',') if f.get('tags') else [],
                'difficulty': f.get('difficulty', '中等'),
                'created_at': f.get('created_at', ''),
                'review_count': f.get('review_count', 0),
                'ease_factor': f.get('ease_factor', 2.5),
                'interval': f.get('interval', 0),
                'next_review': f.get('next_review', ''),
                'last_reviewed': f.get('last_reviewed', ''),
                'last_memory_level': f.get('last_memory_level', '')  # 上次記憶程度
            })
        return notes
    
    def update_note(self, note_id: str, updates: dict) -> bool:
        """更新筆記"""
        try:
            self.table.update(note_id, updates)
            return True
        except Exception as e:
            print(f"更新錯誤: {e}")
            return False
    
    def delete_note(self, note_id: str, user_id: str) -> bool:
        """刪除筆記（驗證使用者）"""
        try:
            notes = self.get_all_notes(user_id)
            note = next((n for n in notes if n['id'] == note_id), None)
            if not note:
                print("❌ 權限錯誤：無法刪除其他使用者的筆記")
                return False
            
            self.table.delete(note_id)
            print(f"✅ 筆記已刪除：{note_id}")
            return True
        except Exception as e:
            print(f"刪除錯誤: {e}")
            return False
    
    def calculate_next_review(self, note: dict, memory_level: str, user_id: str = None) -> dict:
        """計算複習時間（使用自訂間隔設定）
        
        Args:
            memory_level: 記憶程度（中文）- 完全不記得、有點印象、大致記得、很熟悉、完全精通
            user_id: 使用者ID（用於載入自訂設定）
        
        Note:
            記憶程度決定間隔序列（可自訂），筆記難度調整間隔倍率
        """
        # 向後相容：自動遷移舊的記憶程度值
        migration_map = {
            '再次': '完全不記得',
            '困難': '有點印象',
            '良好': '大致記得',
            '容易': '很熟悉',
            '精通': '完全精通'
        }
        
        if memory_level in migration_map:
            memory_level = migration_map[memory_level]
        
        ease_factor = note.get('ease_factor', 2.5)
        interval = note.get('interval', 0)
        review_count = note.get('review_count', 0)
        difficulty = note.get('difficulty', '中等')  # 筆記難度（獨立概念）
        
        # 筆記難度 → 間隔倍率（不變）
        difficulty_multiplier = {
            '極簡單': 1.5,
            '簡單': 1.2,
            '中等': 1.0,
            '困難': 0.8,
            '極困難': 0.6
        }
        multiplier = difficulty_multiplier.get(difficulty, 1.0)
        
        # 載入使用者的間隔設定
        if user_id:
            try:
                from review_settings import ReviewSettings
                settings_manager = ReviewSettings(user_id)
                interval_sequence = settings_manager.get_intervals(memory_level)
            except Exception as e:
                print(f"載入自訂設定失敗，使用預設值：{e}")
                interval_sequence = self._get_default_intervals(memory_level)
        else:
            interval_sequence = self._get_default_intervals(memory_level)
        
        # 記憶程度 → 間隔序列
        if memory_level != '完全不記得':
            if review_count < len(interval_sequence):
                base_interval = interval_sequence[review_count]
            else:
                base_interval = interval_sequence[-1]
            
            # 應用筆記難度倍率
            interval = max(1, int(base_interval * multiplier))
            interval = min(interval, 60)
            
            # 調整 ease_factor
            q = 5 if memory_level in ['完全精通', '很熟悉'] else 4
            ease_factor = ease_factor + (0.1 - (5 - q) * (0.08 + (5 - q) * 0.02))
            ease_factor = max(1.3, ease_factor)
            review_count += 1
        else:
            # 完全不記得：重置
            interval = interval_sequence[0] if interval_sequence else 2
            review_count = 0
            ease_factor = max(1.3, ease_factor - 0.2)
        
        next_review = datetime.now() + timedelta(days=interval)
        
        return {
            'ease_factor': round(ease_factor, 2),
            'interval': interval,
            'review_count': review_count,
            'next_review': next_review.isoformat(),
            'last_reviewed': datetime.now().isoformat(),
            'last_memory_level': memory_level  # 儲存中文記憶程度
        }
    
    def _get_default_intervals(self, memory_level: str) -> list:
        """取得預設間隔序列（備用）"""
        default_intervals = {
            '完全精通': [6, 14, 28, 60, 60],
            '很熟悉': [4, 10, 20, 40, 60],
            '大致記得': [2, 6, 14, 28, 60],
            '有點印象': [2, 4, 8, 16, 30],
            '完全不記得': [2]
        }
    
    def update_review_schedule(self, note_id: str, quality: str, user_id: str) -> bool:
        """更新複習排程"""
        notes = self.get_all_notes(user_id)
        note = next((n for n in notes if n['id'] == note_id), None)
        if not note:
            print(f"❌ 找不到筆記：{note_id}")
            return False
        
        updates = self.calculate_next_review(note, quality, user_id)
        
        try:
            self.table.update(note_id, updates)
            return True
        except Exception as e:
            print(f"❌ 更新失敗：{e}")
            import traceback
            traceback.print_exc()
            return False
    
    def get_due_notes(self, user_id: str) -> list:
        """取得該使用者的到期筆記"""
        notes = self.get_all_notes(user_id)
        now = datetime.now()
        due = []
        
        for note in notes:
            next_review_str = note.get('next_review', '')
            if next_review_str:
                try:
                    next_review = datetime.fromisoformat(next_review_str)
                    if next_review.tzinfo is not None:
                        next_review = next_review.replace(tzinfo=None)
                    
                    if next_review <= now:
                        due.append(note)
                except Exception:
                    pass
        
        return sorted(due, key=lambda x: x.get('next_review', ''))
    
    def get_stats(self, user_id: str) -> dict:
        """統計該使用者的資料"""
        notes = self.get_all_notes(user_id)
        due = self.get_due_notes(user_id)
        
        return {
            'total_notes': len(notes),
            'due_today': len(due),
            'reviewed': len([n for n in notes if n.get('review_count', 0) > 0])
        }