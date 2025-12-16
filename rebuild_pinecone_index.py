"""
Pinecone 索引重建腳本
用於清空並重建 Pinecone 向量資料庫，解決索引損壞或重複向量問題
"""
# -*- coding: utf-8 -*-
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from pinecone import Pinecone
from config import Config
import time

def rebuild_pinecone_index():
    """清空並重建 Pinecone 索引"""
    
    print("=" * 60)
    print("🔄 Pinecone 索引重建工具")
    print("=" * 60)
    print()
    print("⚠️  警告：此操作將刪除所有現有向量！")
    print()
    
    confirm = input("確定要繼續嗎？(輸入 'YES' 確認): ")
    
    if confirm != "YES":
        print("❌ 操作已取消")
        return
    
    try:
        # 初始化 Pinecone
        pc = Pinecone(api_key=Config.PINECONE_API_KEY)
        index = pc.Index(Config.PINECONE_INDEX_NAME)
        
        print()
        print("🗑️  步驟 1: 刪除所有向量...")
        
        # 先檢查索引狀態
        try:
            stats = index.describe_index_stats()
            total_vectors = stats.get('total_vector_count', 0)
            
            if total_vectors == 0:
                print("✅ 索引已經是空的，跳過刪除")
            else:
                print(f"   發現 {total_vectors} 個向量")
                # 刪除所有向量
                try:
                    index.delete(delete_all=True, namespace="")
                    print("✅ 所有向量已刪除")
                except Exception as e:
                    if "Namespace not found" in str(e) or "404" in str(e):
                        print("✅ 索引已經是空的（namespace 不存在）")
                    else:
                        raise e
        except Exception as e:
            if "Namespace not found" in str(e) or "404" in str(e):
                print("✅ 索引已經是空的（namespace 不存在）")
            else:
                raise e
        
        print()
        print("⏳ 等待 5 秒讓索引更新...")
        time.sleep(5)
        
        print()
        print("📊 步驟 2: 檢查索引狀態...")
        stats = index.describe_index_stats()
        print(f"   向量數量: {stats['total_vector_count']}")
        
        if stats['total_vector_count'] == 0:
            print("✅ 索引已清空")
        else:
            print(f"⚠️  警告：索引中還有 {stats['total_vector_count']} 個向量")
        
        print()
        print("=" * 60)
        print("✅ 索引重建完成！")
        print("=" * 60)
        print()
        print("📝 下一步：")
        print("   執行以下命令重新匯入筆記：")
        print("   python import_notes_to_pinecone.py")
        print()
        
    except Exception as e:
        print(f"❌ 發生錯誤：{e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    rebuild_pinecone_index()
