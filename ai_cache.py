"""
AI 回應快取模組
用於快取 AI 生成的內容，加速重複請求的回應時間
"""

import json
import hashlib
import time
from typing import Optional, Dict, Any
from pathlib import Path

class AICache:
    """AI 回應快取管理器"""
    
    def __init__(self, cache_file: str = "ai_cache.json", max_age_hours: int = 24):
        """
        初始化快取管理器
        
        Args:
            cache_file: 快取檔案路徑
            max_age_hours: 快取有效期限（小時）
        """
        self.cache_file = Path(cache_file)
        self.max_age_seconds = max_age_hours * 3600
        self.cache = self._load_cache()
    
    def _load_cache(self) -> Dict:
        """載入快取檔案"""
        if self.cache_file.exists():
            try:
                with open(self.cache_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"⚠️ 載入快取失敗: {e}")
                return {}
        return {}
    
    def _save_cache(self):
        """儲存快取到檔案"""
        try:
            with open(self.cache_file, 'w', encoding='utf-8') as f:
                json.dump(self.cache, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"⚠️ 儲存快取失敗: {e}")
    
    def _generate_key(self, prompt: str, **kwargs) -> str:
        """
        生成快取鍵值
        
        Args:
            prompt: AI prompt
            **kwargs: 其他參數（如 model, temperature 等）
        
        Returns:
            快取鍵值（MD5 hash）
        """
        # 將 prompt 和參數組合成字串
        key_data = f"{prompt}_{json.dumps(kwargs, sort_keys=True)}"
        return hashlib.md5(key_data.encode('utf-8')).hexdigest()
    
    def get(self, prompt: str, **kwargs) -> Optional[str]:
        """
        從快取中取得 AI 回應
        
        Args:
            prompt: AI prompt
            **kwargs: 其他參數
        
        Returns:
            快取的回應，如果不存在或過期則返回 None
        """
        key = self._generate_key(prompt, **kwargs)
        
        if key in self.cache:
            entry = self.cache[key]
            age = time.time() - entry['timestamp']
            
            # 檢查是否過期
            if age < self.max_age_seconds:
                print(f"✅ 快取命中！節省 AI 呼叫時間")
                return entry['response']
            else:
                # 過期，刪除
                del self.cache[key]
                self._save_cache()
        
        return None
    
    def set(self, prompt: str, response: str, **kwargs):
        """
        將 AI 回應存入快取
        
        Args:
            prompt: AI prompt
            response: AI 回應
            **kwargs: 其他參數
        """
        key = self._generate_key(prompt, **kwargs)
        
        self.cache[key] = {
            'response': response,
            'timestamp': time.time(),
            'prompt_preview': prompt[:100]  # 儲存前 100 字元以便除錯
        }
        
        self._save_cache()
    
    def clear_expired(self):
        """清除所有過期的快取項目"""
        current_time = time.time()
        expired_keys = []
        
        for key, entry in self.cache.items():
            age = current_time - entry['timestamp']
            if age >= self.max_age_seconds:
                expired_keys.append(key)
        
        for key in expired_keys:
            del self.cache[key]
        
        if expired_keys:
            self._save_cache()
            print(f"🗑️ 清除了 {len(expired_keys)} 個過期快取項目")
    
    def clear_all(self):
        """清除所有快取"""
        self.cache = {}
        self._save_cache()
        print("🗑️ 已清除所有快取")
    
    def get_stats(self) -> Dict[str, Any]:
        """取得快取統計資訊"""
        total = len(self.cache)
        expired = 0
        current_time = time.time()
        
        for entry in self.cache.values():
            age = current_time - entry['timestamp']
            if age >= self.max_age_seconds:
                expired += 1
        
        return {
            'total_entries': total,
            'valid_entries': total - expired,
            'expired_entries': expired,
            'cache_file': str(self.cache_file),
            'max_age_hours': self.max_age_seconds / 3600
        }
