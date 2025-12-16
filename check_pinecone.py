"""
檢查 Pinecone 索引狀態
"""
# -*- coding: utf-8 -*-
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from ai_core import AICore

ai_core = AICore()

# 檢查索引統計
stats = ai_core.get_index_stats()
print("=" * 60)
print("📊 Pinecone 索引狀態")
print("=" * 60)
print(f"總向量數: {stats['total_vectors']}")
print(f"維度: {stats['dimension']}")
print(f"索引使用率: {stats['index_fullness']}")
print()

if stats['total_vectors'] == 0:
    print("⚠️ 索引是空的！請執行：")
    print("   python import_notes_to_pinecone.py")
else:
    print(f"✅ 索引中有 {stats['total_vectors']} 個向量")
    print()
    print("測試搜尋...")
    
    # 測試搜尋
    test_queries = ["比例原則", "民法", "刑法"]
    
    for query in test_queries:
        print(f"\n🔍 搜尋：{query}")
        results = ai_core.search_knowledge_base(query, top_k=5)
        
        if results:
            print(f"   找到 {len(results)} 個結果")
            for i, r in enumerate(results, 1):
                print(f"   {i}. {r['metadata'].get('title')} (分數: {r['score']:.3f})")
        else:
            print("   ❌ 沒有找到結果")

print("\n" + "=" * 60)
