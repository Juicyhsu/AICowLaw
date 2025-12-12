"""
複習間隔設定模組 - Airtable 雲端版（保留原UI介面）
管理使用者的複習間隔設定，支援預設模板和多個自訂模板
"""

import json
from typing import Dict, List
from config import Config
from pyairtable import Api

# 預設模板定義
PRESET_TEMPLATES = {
    "intensive": {
        "name": "🔥 密集複習",
        "description": "適合考前衝刺，複習頻率較高",
        "intervals": {
            "完全精通": [3, 7, 14, 30, 60],
            "很熟悉": [2, 5, 10, 20, 40],
            "大致記得": [1, 3, 7, 14, 30],
            "有點印象": [1, 2, 4, 8, 16],
            "完全不記得": [1]
        }
    },
    "standard": {
        "name": "📚 標準複習",
        "description": "平衡的複習頻率，適合日常學習",
        "intervals": {
            "完全精通": [6, 14, 28, 60, 60],
            "很熟悉": [4, 10, 20, 40, 60],
            "大致記得": [2, 6, 14, 28, 60],
            "有點印象": [2, 4, 8, 16, 30],
            "完全不記得": [2]
        }
    },
    "relaxed": {
        "name": "🌟 輕鬆複習",
        "description": "複習間隔較長，適合平時鞏固",
        "intervals": {
            "完全精通": [7, 21, 45, 60, 60],
            "很熟悉": [5, 14, 30, 60, 60],
            "大致記得": [3, 7, 14, 30, 60],
            "有點印象": [3, 6, 12, 24, 45],
            "完全不記得": [3]
        }
    }
}

class ReviewSettings:
    """複習設定管理類 - Airtable 版本（保留原UI功能）"""
    
    def __init__(self, user_id: str):
        self.user_id = user_id
        try:
            self.api = Api(Config.AIRTABLE_API_KEY)
            self.table = self.api.table(Config.AIRTABLE_BASE_ID, 'ReviewSettings')
        except Exception as e:
            print(f"⚠️ ReviewSettings Table 不存在，將使用預設設定：{e}")
            self.table = None
    
    def load_settings(self) -> Dict:
        """載入使用者設定"""
        if not self.table:
            return self._get_default_settings()
        
        try:
            formula = f"{{user_id}}='{self.user_id}'"
            records = self.table.all(formula=formula)
            
            if records:
                settings_data = records[0]['fields'].get('settings', '{}')
                settings = json.loads(settings_data)
                return settings
            else:
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
            formula = f"{{user_id}}='{self.user_id}'"
            records = self.table.all(formula=formula)
            
            settings_json = json.dumps(settings, ensure_ascii=False)
            
            if records:
                record_id = records[0]['id']
                self.table.update(record_id, {'settings': settings_json})
            else:
                self.table.create({
                    'user_id': self.user_id,
                    'settings': settings_json
                })
            
            return True
        except Exception as e:
            print(f"❌ 儲存設定失敗：{e}")
            return False
    
    def _get_default_settings(self) -> Dict:
        """取得預設設定"""
        return {
            "active_template": "standard",
            "custom_templates": {}
        }
    
    def get_intervals(self, memory_level: str) -> List[int]:
        """取得指定記憶程度的間隔序列"""
        settings = self.load_settings()
        active_template = settings.get("active_template", "standard")
        
        # 檢查是否為預設模板
        if active_template in PRESET_TEMPLATES:
            intervals = PRESET_TEMPLATES[active_template]["intervals"]
        else:
            # 自訂模板
            custom_templates = settings.get("custom_templates", {})
            if active_template in custom_templates:
                intervals = custom_templates[active_template]["intervals"]
            else:
                # 找不到，使用標準模式
                intervals = PRESET_TEMPLATES["standard"]["intervals"]
        
        return intervals.get(memory_level, [2, 6, 14, 28, 60])
    
    def get_all_templates(self) -> Dict:
        """取得所有可用的模板（預設 + 自訂）"""
        settings = self.load_settings()
        custom_templates = settings.get("custom_templates", {})
        
        # 合併預設和自訂模板
        all_templates = PRESET_TEMPLATES.copy()
        all_templates.update(custom_templates)
        
        return all_templates
    
    def set_active_template(self, template_id: str) -> bool:
        """設定啟用的模板"""
        settings = self.load_settings()
        settings["active_template"] = template_id
        return self.save_settings(settings)
    
    def add_custom_template(self, template_name: str, intervals: Dict[str, List[int]], 
                           description: str = "") -> bool:
        """新增自訂模板"""
        settings = self.load_settings()
        
        if "custom_templates" not in settings:
            settings["custom_templates"] = {}
        
        # 使用名稱作為 key
        template_key = template_name
        settings["custom_templates"][template_key] = {
            "name": template_name,
            "description": description,
            "intervals": intervals
        }
        
        return self.save_settings(settings)
    
    def delete_custom_template(self, template_key: str) -> bool:
        """刪除自訂模板"""
        settings = self.load_settings()
        
        if "custom_templates" in settings and template_key in settings["custom_templates"]:
            del settings["custom_templates"][template_key]
            
            # 如果刪除的是當前啟用的模板，切換到標準模式
            if settings.get("active_template") == template_key:
                settings["active_template"] = "standard"
            
            return self.save_settings(settings)
        
        return False
    
    def update_custom_template(self, template_key: str, name: str, intervals: Dict[str, List[int]],
                              description: str = "") -> bool:
        """更新自訂模板"""
        settings = self.load_settings()
        
        if "custom_templates" in settings and template_key in settings["custom_templates"]:
            settings["custom_templates"][template_key] = {
                "name": name,
                "description": description,
                "intervals": intervals
            }
            return self.save_settings(settings)
        
        return False
