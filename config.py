"""
配置檔 - 包含 Airtable 設定
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# 明確指定 .env 檔案路徑
env_path = Path(__file__).parent / '.env'
load_dotenv(env_path)

# 除錯用：確認有讀到
print(f".env 路徑: {env_path}")
print(f"檔案存在: {env_path.exists()}")

class Config:
    # API 金鑰
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', '')
    PINECONE_API_KEY = os.getenv('PINECONE_API_KEY', '')
    AIRTABLE_API_KEY = os.getenv('AIRTABLE_API_KEY', '')
    AIRTABLE_BASE_ID = os.getenv('AIRTABLE_BASE_ID', '')
    AIRTABLE_TABLE_NAME = 'Notes'
    
    # 科目列表
    SUBJECTS = [
        "民法", "民訴法", "刑法", "刑訴法", "憲法", "行政法",
        "公司法", "證交法", "保險法", "票據法", "強執法",
        "國私法", "國公法", "法律倫理", "法學英文",
        "智財法", "海商海洋法", "勞社法", "財稅法", "其他"
    ]
    
    # Pinecone
    PINECONE_INDEX_NAME = 'legal-exam'
    EMBEDDING_DIMENSION = 768
    
    # Gemini - 使用穩定快速的模型
    GEMINI_MODEL = 'gemini-1.5-flash'
    EMBEDDING_MODEL = 'models/text-embedding-004'
    
    # 系統參數
    MAX_SEARCH_RESULTS = 5
    SIMILARITY_THRESHOLD = 0.5  # 降低閾值以提高搜尋結果數量，同時保持相關性
    EASE_FACTOR_DEFAULT = 2.5
    
    # UI
    PAGE_TITLE = "法律考試 AI 助手"
    PAGE_ICON = "⚖️"
    
    @classmethod
    def validate(cls):
        errors = []
        if not cls.GEMINI_API_KEY:
            errors.append("缺少 GEMINI_API_KEY")
        if not cls.PINECONE_API_KEY:
            errors.append("缺少 PINECONE_API_KEY")
        if not cls.AIRTABLE_API_KEY:
            errors.append("缺少 AIRTABLE_API_KEY")
        if not cls.AIRTABLE_BASE_ID:
            errors.append("缺少 AIRTABLE_BASE_ID")
        
        if errors:
            raise ValueError(f"配置錯誤: {', '.join(errors)}")
        return True