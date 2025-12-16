# -*- coding: utf-8 -*-
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

"""
診斷 Embedding 向量品質
測試 Gemini Embedding API 是否正常工作
"""

from ai_core import AICore
import numpy as np

print("=" * 60)
print("Embedding Quality Diagnostic Tool")
print("=" * 60)

ai_core = AICore()

# 測試 1: 生成相同文字的 embedding，應該完全一樣
print("\n[Test 1] Same text should produce identical embeddings")
text = "比例原則是行政法的重要原則"
emb1 = ai_core.generate_embedding(text, task_type="retrieval_document")
emb2 = ai_core.generate_embedding(text, task_type="retrieval_document")

similarity = np.dot(emb1, emb2) / (np.linalg.norm(emb1) * np.linalg.norm(emb2))
print(f"Similarity: {similarity:.6f}")
if similarity > 0.999:
    print("[OK] Embeddings are consistent")
else:
    print("[ERROR] Embeddings are inconsistent!")

# 測試 2: 相關文字應該有高相似度
print("\n[Test 2] Related texts should have high similarity")
text1 = "比例原則是行政法的重要原則"
text2 = "行政法中的比例原則包含適當性、必要性和狹義比例原則"

emb1 = ai_core.generate_embedding(text1, task_type="retrieval_document")
emb2 = ai_core.generate_embedding(text2, task_type="retrieval_document")

similarity = np.dot(emb1, emb2) / (np.linalg.norm(emb1) * np.linalg.norm(emb2))
print(f"Text 1: {text1}")
print(f"Text 2: {text2}")
print(f"Similarity: {similarity:.6f}")
if similarity > 0.7:
    print("[OK] Related texts have high similarity")
else:
    print("[WARNING] Similarity is lower than expected")

# 測試 3: 不相關文字應該有低相似度
print("\n[Test 3] Unrelated texts should have low similarity")
text1 = "比例原則是行政法的重要原則"
text2 = "特留分是繼承法中保障繼承人的制度"

emb1 = ai_core.generate_embedding(text1, task_type="retrieval_document")
emb2 = ai_core.generate_embedding(text2, task_type="retrieval_document")

similarity = np.dot(emb1, emb2) / (np.linalg.norm(emb1) * np.linalg.norm(emb2))
print(f"Text 1: {text1}")
print(f"Text 2: {text2}")
print(f"Similarity: {similarity:.6f}")
if similarity < 0.5:
    print("[OK] Unrelated texts have low similarity")
else:
    print("[WARNING] Similarity is higher than expected")

# 測試 4: 測試 retrieval_query vs retrieval_document
print("\n[Test 4] Query vs Document task_type")
query = "比例原則"
doc = "比例原則是行政法的重要原則，包含適當性、必要性和狹義比例原則三個子原則"

query_emb = ai_core.generate_embedding(query, task_type="retrieval_query")
doc_emb = ai_core.generate_embedding(doc, task_type="retrieval_document")

similarity = np.dot(query_emb, doc_emb) / (np.linalg.norm(query_emb) * np.linalg.norm(doc_emb))
print(f"Query: {query}")
print(f"Document: {doc}")
print(f"Similarity: {similarity:.6f}")
if similarity > 0.7:
    print("[OK] Query-Document matching works well")
else:
    print("[WARNING] Query-Document similarity is low")

print("\n" + "=" * 60)
print("Diagnostic Complete")
print("=" * 60)
