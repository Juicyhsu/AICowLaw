"""
自訂風格儲存管理
使用 JSON 文件儲存使用者的自訂筆記風格
"""

import json
import os
from typing import Dict

STYLE_FILE = "user_styles.json"

def load_user_styles(user_id: str) -> Dict[str, str]:
    """載入使用者的自訂風格
    
    Args:
        user_id: 使用者 ID
        
    Returns:
        風格名稱 -> 風格描述的字典
    """
    if not os.path.exists(STYLE_FILE):
        return {}
    
    try:
        with open(STYLE_FILE, 'r', encoding='utf-8') as f:
            all_styles = json.load(f)
            return all_styles.get(user_id, {})
    except Exception as e:
        print(f"載入風格失敗: {e}")
        return {}

def save_user_style(user_id: str, style_name: str, style_description: str) -> bool:
    """儲存使用者的自訂風格
    
    Args:
        user_id: 使用者 ID
        style_name: 風格名稱
        style_description: 風格描述
        
    Returns:
        是否成功
    """
    try:
        # 載入現有資料
        all_styles = {}
        if os.path.exists(STYLE_FILE):
            with open(STYLE_FILE, 'r', encoding='utf-8') as f:
                all_styles = json.load(f)
        
        # 更新該使用者的風格
        if user_id not in all_styles:
            all_styles[user_id] = {}
        
        all_styles[user_id][style_name] = style_description
        
        # 儲存回檔案
        with open(STYLE_FILE, 'w', encoding='utf-8') as f:
            json.dump(all_styles, f, ensure_ascii=False, indent=2)
        
        return True
    except Exception as e:
        print(f"儲存風格失敗: {e}")
        return False

def delete_user_style(user_id: str, style_name: str) -> bool:
    """刪除使用者的自訂風格
    
    Args:
        user_id: 使用者 ID
        style_name: 風格名稱
        
    Returns:
        是否成功
    """
    try:
        if not os.path.exists(STYLE_FILE):
            return False
        
        with open(STYLE_FILE, 'r', encoding='utf-8') as f:
            all_styles = json.load(f)
        
        if user_id in all_styles and style_name in all_styles[user_id]:
            del all_styles[user_id][style_name]
            
            # 儲存回檔案
            with open(STYLE_FILE, 'w', encoding='utf-8') as f:
                json.dump(all_styles, f, ensure_ascii=False, indent=2)
            
            return True
        return False
    except Exception as e:
        print(f"刪除風格失敗: {e}")
        return False

def get_all_style_names(user_id: str) -> list:
    """取得使用者所有自訂風格的名稱
    
    Args:
        user_id: 使用者 ID
        
    Returns:
        風格名稱列表
    """
    styles = load_user_styles(user_id)
    return list(styles.keys())
