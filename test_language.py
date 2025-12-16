# -*- coding: utf-8 -*-
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

"""
測試英文 vs 中文 embedding
"""

import google.generativeai as genai
from config import Config
import numpy as np

genai.configure(api_key=Config.GEMINI_API_KEY)

print("=" * 60)
print("Language Test: English vs Chinese")
print("=" * 60)

# 測試英文
print("\n[Test 1] English texts")
text1_en = "The principle of proportionality is an important principle in administrative law"
text2_en = "Reserved portion is a system to protect heirs in inheritance law"

result1 = genai.embed_content(
    model=Config.EMBEDDING_MODEL,
    content=text1_en,
    task_type="retrieval_document"
)

result2 = genai.embed_content(
    model=Config.EMBEDDING_MODEL,
    content=text2_en,
    task_type="retrieval_document"
)

emb1 = result1['embedding']
emb2 = result2['embedding']

sim = np.dot(emb1, emb2) / (np.linalg.norm(emb1) * np.linalg.norm(emb2))

print(f"Text 1: {text1_en}")
print(f"  First 5: {emb1[:5]}")
print(f"Text 2: {text2_en}")
print(f"  First 5: {emb2[:5]}")
print(f"Similarity: {sim:.6f}")

if abs(sim - 1.0) < 0.001:
    print("⚠️ 警告：向量完全相同！")
else:
    print("✅ 向量不同")

# 測試中文
print("\n[Test 2] Chinese texts")
text1_zh = "比例原則是行政法的重要原則"
text2_zh = "特留分是繼承法中保障繼承人的制度"

result1 = genai.embed_content(
    model=Config.EMBEDDING_MODEL,
    content=text1_zh,
    task_type="retrieval_document"
)

result2 = genai.embed_content(
    model=Config.EMBEDDING_MODEL,
    content=text2_zh,
    task_type="retrieval_document"
)

emb1 = result1['embedding']
emb2 = result2['embedding']

sim = np.dot(emb1, emb2) / (np.linalg.norm(emb1) * np.linalg.norm(emb2))

print(f"Text 1: {text1_zh}")
print(f"  First 5: {emb1[:5]}")
print(f"Text 2: {text2_zh}")
print(f"  First 5: {emb2[:5]}")
print(f"Similarity: {sim:.6f}")

if abs(sim - 1.0) < 0.001:
    print("⚠️ 警告：向量完全相同！")
else:
    print("✅ 向量不同")

print("\n" + "=" * 60)
