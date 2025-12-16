# -*- coding: utf-8 -*-
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

"""
完全刪除並重新創建 Pinecone 索引（新維度）
"""

from pinecone import Pinecone, ServerlessSpec
from config import Config
import time

print("=" * 60)
print("Pinecone Index Recreation (New Dimension)")
print("=" * 60)

# 初始化 Pinecone
pc = Pinecone(api_key=Config.PINECONE_API_KEY)

index_name = Config.PINECONE_INDEX_NAME

print(f"\n檢查索引 '{index_name}' 是否存在...")

# 檢查索引是否存在
existing_indexes = pc.list_indexes()
index_exists = any(idx['name'] == index_name for idx in existing_indexes)

if index_exists:
    print(f"✅ 索引存在，準備刪除...")
    
    confirm = input(f"確定要刪除索引 '{index_name}' 嗎？(輸入 'YES' 確認): ")
    
    if confirm == 'YES':
        print(f"🗑️  刪除索引...")
        pc.delete_index(index_name)
        print(f"✅ 索引已刪除")
        
        print("⏳ 等待 10 秒...")
        time.sleep(10)
    else:
        print("❌ 取消操作")
        exit(0)
else:
    print(f"ℹ️  索引不存在")

# 創建新索引（1536 維度）
print(f"\n📦 創建新索引（維度: {Config.EMBEDDING_DIMENSION}）...")

pc.create_index(
    name=index_name,
    dimension=Config.EMBEDDING_DIMENSION,
    metric='cosine',
    spec=ServerlessSpec(
        cloud='aws',
        region='us-east-1'
    )
)

print("✅ 新索引已創建")

print("\n⏳ 等待索引準備就緒...")
time.sleep(10)

# 驗證
index = pc.Index(index_name)
stats = index.describe_index_stats()

print("\n" + "=" * 60)
print("索引資訊")
print("=" * 60)
print(f"名稱: {index_name}")
print(f"維度: {stats.get('dimension', 'N/A')}")
print(f"向量數: {stats.get('total_vector_count', 0)}")
print("=" * 60)

print("\n✅ 完成！現在可以執行 import_notes_to_pinecone.py")
