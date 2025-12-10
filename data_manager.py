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
                  tags: list = None, difficulty: str = "中等") -> dict:
        """儲存筆記到 Airtable"""
        note = {
            'user_id': user_id,
            'title': title,
            'content': content,
            'category': category,
            'tags': ','.join(tags) if tags else '',
            'difficulty': difficulty,  # 改為 difficulty
            'review_count': 0,
            'ease_factor': Config.EASE_FACTOR_DEFAULT,
            'interval': 0,
            'next_review': datetime.now().isoformat()
        }
        result = self.table.create(note)
        print(f"✅ 筆記已儲存：{title}")
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
                'difficulty': f.get('difficulty', '中等'),  # 改為 difficulty
                'created_at': f.get('created_at', ''),
                'review_count': f.get('review_count', 0),
                'ease_factor': f.get('ease_factor', 2.5),
                'interval': f.get('interval', 0),
                'next_review': f.get('next_review', ''),
                'last_reviewed': f.get('last_reviewed', '')
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
    
    def calculate_next_review(self, note: dict, quality: str) -> dict:
        """SM-2 演算法計算複習時間"""
        quality_map = {'再次': 0, '困難': 3, '良好': 4, '容易': 5, '精通': 5}
        q = quality_map.get(quality, 3)
        
        ease_factor = note.get('ease_factor', 2.5)
        interval = note.get('interval', 0)
        review_count = note.get('review_count', 0)
        
        if q >= 3:
            if review_count == 0:
                interval = 1
            elif review_count == 1:
                interval = 6
            else:
                interval = math.ceil(interval * ease_factor)
            
            if quality == '精通':
                interval = max(interval, 30)
            
            ease_factor = ease_factor + (0.1 - (5 - q) * (0.08 + (5 - q) * 0.02))
            ease_factor = max(1.3, ease_factor)
            review_count += 1
        else:
            interval = 1
            review_count = 0
            ease_factor = max(1.3, ease_factor - 0.2)
        
        next_review = datetime.now() + timedelta(days=interval)
        
        return {
            'ease_factor': round(ease_factor, 2),
            'interval': interval,
            'review_count': review_count,
            'next_review': next_review.isoformat(),
            'last_reviewed': datetime.now().isoformat()
        }
    
    def update_review_schedule(self, note_id: str, quality: str, user_id: str) -> bool:
        """更新複習排程"""
        notes = self.get_all_notes(user_id)
        note = next((n for n in notes if n['id'] == note_id), None)
        if not note:
            print(f"❌ 找不到筆記：{note_id}")
            return False
        
        updates = self.calculate_next_review(note, quality)
        
        try:
            self.table.update(note_id, updates)
            print(f"✅ 已更新複習排程：{note.get('title')} - 下次複習：{updates['interval']}天後，複習次數：{updates['review_count']}")
            return True
        except Exception as e:
            print(f"❌ 更新失敗：{e}")
            return False
    
    def get_due_notes(self, user_id: str) -> list:
        """取得該使用者的到期筆記"""
        notes = self.get_all_notes(user_id)
        now = datetime.now()
        due = []
        
        for note in notes:
            try:
                next_review_str = note.get('next_review', '')
                if not next_review_str:
                    # 新筆記沒有 next_review，不應該立即加入複習列表
                    # 只有已經複習過至少一次的筆記才會有 next_review
                    continue
                
                next_review = datetime.fromisoformat(next_review_str)
                if next_review <= now:
                    due.append(note)
            except Exception as e:
                print(f"⚠️ 解析 next_review 錯誤：{e}")
                # 解析錯誤的筆記也不加入複習列表
                continue
        
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