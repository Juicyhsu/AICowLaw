# 🔄 簡化的開發流程

## 📌 現在只有一個部署分支

為了避免混亂，我們簡化成：

### ✅ main 分支（唯一部署分支）
- 使用 OpenAI Whisper API
- 部署到 Zeabur
- 你在電腦上開發也用這個

### 📁 local 分支（備份）
- 本地 Whisper 版本
- 保留作為參考
- 不再主動維護

---

## 🛠️ 以後的開發流程

### 1. 在電腦上修改程式碼
```bash
# 確認在 main 分支
git checkout main

# 修改 app.py 或其他檔案
# ...

# 測試
streamlit run app.py
```

### 2. 提交並推送
```bash
git add .
git commit -m "描述你的修改"
git push
```

### 3. Zeabur 自動部署
- Zeabur 會自動偵測 GitHub 更新
- 自動重新部署
- 等待 3-5 分鐘

---

## ⚠️ 重要提醒

### 環境變數
**本地開發**：使用 `.env` 檔案
```
GEMINI_API_KEY=你的金鑰
PINECONE_API_KEY=你的金鑰
AIRTABLE_API_KEY=你的金鑰
AIRTABLE_BASE_ID=你的BaseID
OPENAI_API_KEY=你的OpenAI金鑰
```

**Zeabur 部署**：在 Zeabur 設定環境變數（PRIVATE）

### 語音功能
- 本地開發：需要 OpenAI API Key
- Zeabur 部署：需要 OpenAI API Key
- 都是用 OpenAI Whisper API（付費但便宜）

---

## 🐛 剛修復的 Bug

**問題**：`ModuleNotFoundError: No module named 'custom_style_manager'`

**原因**：程式碼引用了已刪除的 `custom_style_manager.py`

**解決**：移除該依賴，簡化風格選擇

**狀態**：✅ 已修復並推送

---

## 📝 快速參考

```bash
# 查看目前分支
git branch

# 查看狀態
git status

# 提交修改
git add .
git commit -m "修改說明"
git push

# 如果需要本地免費版本
git checkout local
```

---

**現在流程很簡單：修改 → 提交 → 推送 → 自動部署！** 🚀
