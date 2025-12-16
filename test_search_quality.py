# -*- coding: utf-8 -*-
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

"""
測試 OpenAI embeddings 搜尋品質
"""

from ai_core import AICore

print("=" * 60)
print("Search Quality Test with OpenAI Embeddings")
print("=" * 60)

ai_core = AICore()

# 測試搜尋
test_queries = [
    "比例原則",
    "民法",
    "行政法",
    "特留分"
]

for query in test_queries:
    print(f"\n{'='*60}")
    print(f"搜尋：{query}")
    print('='*60)
    
    results = ai_core.search_knowledge_base(query, top_k=5)
    
    if results:
        print(f"✅ 找到 {len(results)} 個結果\n")
        for i, r in enumerate(results, 1):
            print(f"{i}. {r['metadata'].get('title', 'N/A')}")
            print(f"   相似度: {r['score']:.4f}")
            print(f"   分類: {r['metadata'].get('category', 'N/A')}")
            print()
    else:
        print("❌ 沒有找到結果\n")

print("=" * 60)
print("測試完成")
print("=" * 60)
