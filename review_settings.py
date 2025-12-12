"""
複習間隔設定管理 - Airtable 雲端版
支援本地端和雲端同步
"""

import json
from typing import Dict
from config import Config
from pyairtable import Api

class ReviewSettings:
    """複習間隔設定管理器（Airtable 版本）"""
    
    # 預設間隔設定
    DEFAULT_INTERVALS = {
        '完全精通': [6, 14, 28, 60, 60],
        '很熟悉': [4, 10, 20, 40, 60],
        '大致記得': [2, 6, 14, 28, 60],
        '有點印象': [2, 4, 8, 16, 30],
        '完全不記得': [2]
    }
    
    def __init__(self, user_id: str):
        """
        初始化設定管理器
        
        Args:
            user_id: 使用者 ID
        """
        self.user_id = user_id
        self.api = Api(Config.AIRTABLE_API_KEY)
        
        # 使用 ReviewSettings Table（需要在 Airtable 建立）
        try:
            self.table = self.api.table(Config.AIRTABLE_BASE_ID, 'ReviewSettings')
        except Exception as e:
            print(f"⚠️ ReviewSettings Table 不存在，將使用預設設定：{e}")
            self.table = None
    
    def load_settings(self) -> Dict:
        """載入使用者設定"""
        if not self.table:
            return self._get_default_settings()
        
        try:
            # 從 Airtable 查詢該使用者的設定
            formula = f"{{user_id}}='{self.user_id}'"
            records = self.table.all(formula=formula)
            
            if records:
                # 取得第一筆記錄
                settings_data = records[0]['fields'].get('settings', '{}')
                settings = json.loads(settings_data)
                print(f"✅ 從 Airtable 載入 {self.user_id} 的設定")
                return settings
            else:
                # 沒有設定，使用預設值
                print(f"ℹ️ {self.user_id} 尚無自訂設定，使用預設值")
                return self._get_default_settings()
                
        except Exception as e:
            print(f"⚠️ 載入設定失敗，使用預設值：{e}")
            return self._get_default_settings()
    
    def save_settings(self, settings: Dict) -> bool:
        """儲存使用者設定到 Airtable"""
        if not self.table:
            print("⚠️ ReviewSettings Table 不存在，無法儲存")
            return False
        
        try:
            # 檢查是否已有記錄
            formula = f"{{user_id}}='{self.user_id}'"
            records = self.table.all(formula=formula)
            
            settings_json = json.dumps(settings, ensure_ascii=False)
            
            if records:
                # 更新現有記錄
                record_id = records[0]['id']
                self.table.update(record_id, {'settings': settings_json})
                print(f"✅ 更新 {self.user_id} 的設定到 Airtable")
            else:
                # 建立新記錄
                self.table.create({
                    'user_id': self.user_id,
                    'settings': settings_json
                })
                print(f"✅ 建立 {self.user_id} 的設定到 Airtable")
            
            return True
            
        except Exception as e:
            print(f"❌ 儲存設定失敗：{e}")
            return False
    
    def _get_default_settings(self) -> Dict:
        """取得預設設定"""
        return {
            'intervals': self.DEFAULT_INTERVALS.copy(),
            'mode': '標準複習'
        }
    
    def get_intervals(self, memory_level: str) -> list:
        """
        取得指定記憶程度的間隔序列
        
        Args:
            memory_level: 記憶程度（中文）
        
        Returns:
            間隔序列（天數列表）
        """
        settings = self.load_settings()
        intervals = settings.get('intervals', {})
        
        # 取得該記憶程度的間隔，如果沒有則使用預設值
        return intervals.get(memory_level, self.DEFAULT_INTERVALS.get(memory_level, [2]))
    
    def update_intervals(self, memory_level: str, intervals: list) -> bool:
        """
        更新指定記憶程度的間隔序列
        
        Args:
            memory_level: 記憶程度
            intervals: 新的間隔序列
        
        Returns:
            是否成功
        """
        settings = self.load_settings()
        
        if 'intervals' not in settings:
            settings['intervals'] = self.DEFAULT_INTERVALS.copy()
        
        settings['intervals'][memory_level] = intervals
        
        return self.save_settings(settings)
    
    def reset_to_default(self) -> bool:
        """重置為預設設定"""
        return self.save_settings(self._get_default_settings())
    
    def get_all_intervals(self) -> Dict[str, list]:
        """取得所有記憶程度的間隔設定"""
        settings = self.load_settings()
        return settings.get('intervals', self.DEFAULT_INTERVALS.copy())
    
    def update_all_intervals(self, all_intervals: Dict[str, list]) -> bool:
        """
        更新所有間隔設定
        
        Args:
            all_intervals: 所有記憶程度的間隔設定
        
        Returns:
            是否成功
        """
        settings = self.load_settings()
        settings['intervals'] = all_intervals
        return self.save_settings(settings)
