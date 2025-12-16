# -*- coding: utf-8 -*-
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

"""
更詳細的中文測試
"""

import google.generativeai as genai
from config import Config
import numpy as np

genai.configure(api_key=Config.GEMINI_API_KEY)

print("=" * 60)
print("Detailed Chinese Text Test")
print("=" * 60)

# 測試多個完全不同的中文文字
texts = [
    "比例原則",
    "特留分",
    "民法",
    "刑法",
    "行政法",
    "今天天氣很好",
    "我喜歡吃蘋果",
    "電腦很重要",
    "法律是社會規範"
]

print("\n生成 embeddings...")
embeddings = []
for text in texts:
    result = genai.embed_content(
        model=Config.EMBEDDING_MODEL,
        content=text,
        task_type="retrieval_document"
    )
    embeddings.append(result['embedding'])
    print(f"  {text}: {result['embedding'][:3]}")

# 檢查是否所有向量都相同
print("\n檢查向量是否相同...")
all_same = True
for i in range(1, len(embeddings)):
    if embeddings[i] != embeddings[0]:
        all_same = False
        break

if all_same:
    print("⚠️ 所有向量完全相同！")
else:
    print("✅ 向量不同")
    
    # 計算相似度矩陣
    print("\n相似度矩陣（前5個）:")
    for i in range(min(5, len(texts))):
        for j in range(i+1, min(5, len(texts))):
            sim = np.dot(embeddings[i], embeddings[j]) / (
                np.linalg.norm(embeddings[i]) * np.linalg.norm(embeddings[j])
            )
            print(f"  '{texts[i]}' vs '{texts[j]}': {sim:.4f}")

print("\n" + "=" * 60)
