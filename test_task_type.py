# -*- coding: utf-8 -*-
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

"""
測試不同 task_type 的影響
"""

import google.generativeai as genai
from config import Config
import numpy as np

genai.configure(api_key=Config.GEMINI_API_KEY)

print("=" * 60)
print("Task Type Test")
print("=" * 60)

text1 = "比例原則是行政法的重要原則"
text2 = "特留分是繼承法中保障繼承人的制度"

# 測試不同的 task_type
task_types = [
    "retrieval_document",
    "retrieval_query", 
    "semantic_similarity",
    "classification",
    "clustering"
]

print("\n測試不同 task_type 對中文文字的影響...\n")

for task_type in task_types:
    try:
        print(f"\n[{task_type}]")
        
        result1 = genai.embed_content(
            model=Config.EMBEDDING_MODEL,
            content=text1,
            task_type=task_type
        )
        
        result2 = genai.embed_content(
            model=Config.EMBEDDING_MODEL,
            content=text2,
            task_type=task_type
        )
        
        emb1 = result1['embedding']
        emb2 = result2['embedding']
        
        # 計算相似度
        sim = np.dot(emb1, emb2) / (np.linalg.norm(emb1) * np.linalg.norm(emb2))
        
        print(f"  Text 1 前5值: {emb1[:5]}")
        print(f"  Text 2 前5值: {emb2[:5]}")
        print(f"  相似度: {sim:.6f}")
        
        if abs(sim - 1.0) < 0.001:
            print(f"  ⚠️ 警告：向量完全相同！")
        else:
            print(f"  ✅ 向量不同")
            
    except Exception as e:
        print(f"  ❌ 錯誤: {e}")

print("\n" + "=" * 60)

# 測試不指定 task_type
print("\n測試不指定 task_type...")
try:
    result1 = genai.embed_content(
        model=Config.EMBEDDING_MODEL,
        content=text1
    )
    
    result2 = genai.embed_content(
        model=Config.EMBEDDING_MODEL,
        content=text2
    )
    
    emb1 = result1['embedding']
    emb2 = result2['embedding']
    
    sim = np.dot(emb1, emb2) / (np.linalg.norm(emb1) * np.linalg.norm(emb2))
    
    print(f"Text 1 前5值: {emb1[:5]}")
    print(f"Text 2 前5值: {emb2[:5]}")
    print(f"相似度: {sim:.6f}")
    
    if abs(sim - 1.0) < 0.001:
        print(f"⚠️ 警告：向量完全相同！")
    else:
        print(f"✅ 向量不同")
        
except Exception as e:
    print(f"❌ 錯誤: {e}")

print("\n" + "=" * 60)
