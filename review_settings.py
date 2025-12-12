"""
複習間隔設定模組
管理使用者的複習間隔設定，支援預設模板和多個自訂模板
"""

import json
import os
from typing import Dict, List

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
    """複習設定管理類 - 支援多個自訂模板"""
    
    def __init__(self, user_id: str):
        self.user_id = user_id
        self.settings_file = f"review_settings_{user_id}.json"
    
    def load_settings(self) -> Dict:
        """載入使用者設定"""
        if os.path.exists(self.settings_file):
            try:
                with open(self.settings_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"載入設定失敗：{e}")
                return self._get_default_settings()
        else:
            return self._get_default_settings()
    
    def save_settings(self, settings: Dict) -> bool:
        """儲存使用者設定"""
        try:
            with open(self.settings_file, 'w', encoding='utf-8') as f:
                json.dump(settings, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"儲存設定失敗：{e}")
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
    
    def validate_intervals(self, intervals: Dict[str, List[int]]) -> bool:
        """驗證間隔設定是否合法"""
        required_levels = ["完全精通", "很熟悉", "大致記得", "有點印象", "完全不記得"]
        
        for level in required_levels:
            if level not in intervals:
                return False
            
            level_intervals = intervals[level]
            
            if not isinstance(level_intervals, list) or len(level_intervals) == 0:
                return False
            
            for interval in level_intervals:
                if not isinstance(interval, int) or interval < 1 or interval > 60:
                    return False
        
        return True
    
    def set_active_template(self, template_name: str) -> bool:
        """設定啟用的模板"""
        settings = self.load_settings()
        
        # 檢查模板是否存在
        if template_name in PRESET_TEMPLATES or template_name in settings.get("custom_templates", {}):
            settings["active_template"] = template_name
            return self.save_settings(settings)
        
        return False
    
    def add_custom_template(self, template_name: str, intervals: Dict[str, List[int]]) -> bool:
        """新增自訂模板"""
        if not self.validate_intervals(intervals):
            return False
        
        settings = self.load_settings()
        
        if "custom_templates" not in settings:
            settings["custom_templates"] = {}
        
        settings["custom_templates"][template_name] = {
            "name": template_name,
            "intervals": intervals
        }
        
        return self.save_settings(settings)
    
    def delete_custom_template(self, template_name: str) -> bool:
        """刪除自訂模板"""
        settings = self.load_settings()
        custom_templates = settings.get("custom_templates", {})
        
        if template_name in custom_templates:
            del custom_templates[template_name]
            
            # 如果刪除的是當前啟用的模板，切換到標準模式
            if settings.get("active_template") == template_name:
                settings["active_template"] = "standard"
            
            return self.save_settings(settings)
        
        return False
    
    def get_all_templates(self) -> Dict:
        """取得所有模板（預設+自訂）"""
        settings = self.load_settings()
        
        all_templates = {}
        
        # 預設模板
        for key, template in PRESET_TEMPLATES.items():
            all_templates[key] = {
                "name": template["name"],
                "type": "preset",
                "intervals": template["intervals"]
            }
        
        # 自訂模板
        custom_templates = settings.get("custom_templates", {})
        for key, template in custom_templates.items():
            all_templates[key] = {
                "name": template["name"],
                "type": "custom",
                "intervals": template["intervals"]
            }
        
        return all_templates
