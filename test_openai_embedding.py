# -*- coding: utf-8 -*-
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

"""
測試 OpenAI Embeddings 對中文的處理
"""

from openai import OpenAI
from config import Config
import numpy as np

client = OpenAI(api_key=Config.OPENAI_API_KEY)

print("=" * 60)
print("OpenAI Embeddings Test for Chinese")
print("=" * 60)

texts = [
    "比例原則是行政法的重要原則",
    "特留分是繼承法中保障繼承人的制度",
    "民法規定契約自由原則"
]

print("\n生成 embeddings...")
embeddings = []
for text in texts:
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    emb = response.data[0].embedding
    embeddings.append(emb)
    print(f"  {text}")
    print(f"    維度: {len(emb)}")
    print(f"    前5值: {emb[:5]}")

# 計算相似度
print("\n" + "=" * 60)
print("相似度測試")
print("=" * 60)

for i in range(len(texts)):
    for j in range(i+1, len(texts)):
        sim = np.dot(embeddings[i], embeddings[j]) / (
            np.linalg.norm(embeddings[i]) * np.linalg.norm(embeddings[j])
        )
        print(f"\n'{texts[i]}'")
        print(f"vs")
        print(f"'{texts[j]}'")
        print(f"相似度: {sim:.4f}")
        
        if abs(sim - 1.0) < 0.001:
            print("⚠️ 向量相同！")
        elif sim > 0.8:
            print("✅ 高度相關")
        elif sim > 0.5:
            print("✅ 中度相關")
        else:
            print("✅ 低度相關（正常）")

print("\n" + "=" * 60)
print("結論：OpenAI embeddings 是否能正確處理中文？")
print("=" * 60)

# 檢查是否所有向量都不同
all_different = True
for i in range(len(embeddings)):
    for j in range(i+1, len(embeddings)):
        if embeddings[i] == embeddings[j]:
            all_different = False
            break

if all_different:
    print("✅ 成功！所有中文文字都有不同的向量")
    print("✅ OpenAI embeddings 可以正確處理中文")
else:
    print("⚠️ 失敗：有相同的向量")

print("=" * 60)
