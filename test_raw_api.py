# -*- coding: utf-8 -*-
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

"""
測試 Gemini Embedding API 原始回應
"""

import google.generativeai as genai
from config import Config
import numpy as np

genai.configure(api_key=Config.GEMINI_API_KEY)

print("=" * 60)
print("Raw Gemini API Test")
print("=" * 60)

# 測試 1: 檢查 API 返回的向量
print("\n[Test] Generating embeddings for different texts...")

texts = [
    "比例原則是行政法的重要原則",
    "特留分是繼承法中保障繼承人的制度",
    "民法規定契約自由原則"
]

embeddings = []
for i, text in enumerate(texts, 1):
    result = genai.embed_content(
        model=Config.EMBEDDING_MODEL,
        content=text,
        task_type="retrieval_document"
    )
    emb = result['embedding']
    embeddings.append(emb)
    
    print(f"\nText {i}: {text}")
    print(f"  Vector length: {len(emb)}")
    print(f"  First 5 values: {emb[:5]}")
    print(f"  Vector norm: {np.linalg.norm(emb):.6f}")

# 計算相似度
print("\n" + "=" * 60)
print("Similarity Matrix")
print("=" * 60)

for i in range(len(embeddings)):
    for j in range(i+1, len(embeddings)):
        sim = np.dot(embeddings[i], embeddings[j]) / (
            np.linalg.norm(embeddings[i]) * np.linalg.norm(embeddings[j])
        )
        print(f"Text {i+1} vs Text {j+1}: {sim:.6f}")

print("\n" + "=" * 60)
