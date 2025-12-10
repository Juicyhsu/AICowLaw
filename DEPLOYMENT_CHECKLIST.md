# 📦 部署檔案清單

## ✅ 必須上傳的檔案

### 核心程式碼
- ✅ `app.py` - 主程式
- ✅ `config.py` - 系統配置
- ✅ `ai_core.py` - AI 核心
- ✅ `data_manager.py` - 資料管理
- ✅ `prompt_templates.py` - AI 提示詞模板

### 配置檔案
- ✅ `requirements.txt` - Python 依賴清單
- ✅ `.streamlit/config.toml` - Streamlit 配置（如果有）
- ✅ `.gitignore` - Git 忽略清單

### 文件
- ✅ `README.md` - 專案說明
- ✅ `DEPLOYMENT.md` - 部署指南

---

## ❌ 不要上傳的檔案

### 敏感資訊
- ❌ `.env` - **絕對不要上傳！**（包含 API 金鑰）
- ❌ `.streamlit/secrets.toml` - 本地密鑰

### 快取和臨時檔案
- ❌ `__pycache__/` - Python 快取
- ❌ `*.pyc` - 編譯後的 Python 檔案
- ❌ `test.mp3` - 測試檔案（已刪除）
- ❌ `*.backup*` - 備份檔案
- ❌ `ai_core.py.backup_broken` - 舊備份

### 測試和開發檔案
- ❌ `tests/` - 測試資料夾（可選，看需求）
- ❌ `custom_styles/` - 自訂風格（如果不需要）
- ❌ `custom_style_manager.py` - 風格管理器（如果不需要）

---

## 📋 部署前檢查清單

### 1. 建立 .gitignore
```bash
# 已經幫你建立好了
# 位置：c:\Users\user\Desktop\法烤牛\主程式\.gitignore
```

### 2. 確認 requirements.txt 完整
```txt
streamlit>=1.28.0
google-generativeai>=0.3.0
pinecone-client>=2.2.0
python-dotenv>=1.0.0
pyairtable>=2.1.0
PyMuPDF>=1.23.0
gTTS>=2.4.0
python-docx>=1.1.0
```

### 3. 移除敏感資訊
- [ ] 確認 `.env` 不在 Git 追蹤中
- [ ] 確認程式碼中沒有寫死的 API 金鑰
- [ ] 確認密碼不在程式碼中（使用環境變數）

### 4. 清理不需要的檔案
```bash
# 刪除備份檔案
Remove-Item "*.backup*" -Force

# 清理 Python 快取
Remove-Item "__pycache__" -Recurse -Force
```

---

## 🚀 部署到 GitHub 步驟

### 初始化 Git
```bash
cd "c:\Users\user\Desktop\法烤牛\主程式"
git init
```

### 添加檔案
```bash
# 添加所有檔案（.gitignore 會自動排除不需要的）
git add .

# 檢查將要提交的檔案
git status
```

### 提交
```bash
git commit -m "Initial commit for deployment"
```

### 推送到 GitHub
```bash
# 建立 GitHub Repository 後
git remote add origin https://github.com/你的帳號/legal-exam-ai.git
git branch -M main
git push -u origin main
```

---

## 🌐 部署到 Zeabur

### 1. 連接 GitHub
1. 登入 Zeabur
2. 點擊「New Project」
3. 選擇「Import from GitHub」
4. 選擇你的 Repository

### 2. 設定環境變數
在 Zeabur 設定以下環境變數：
```
GEMINI_API_KEY=你的金鑰
PINECONE_API_KEY=你的金鑰
AIRTABLE_API_KEY=你的金鑰
AIRTABLE_BASE_ID=你的BaseID
```

### 3. 部署
- Zeabur 會自動偵測 `requirements.txt`
- 自動安裝依賴
- 自動啟動應用

---

## 📊 檔案大小參考

| 檔案 | 大小 | 說明 |
|------|------|------|
| app.py | ~103 KB | 主程式 |
| ai_core.py | ~20 KB | AI 核心 |
| data_manager.py | ~7 KB | 資料管理 |
| prompt_templates.py | ~10 KB | 提示詞 |
| config.py | ~2 KB | 配置 |
| requirements.txt | ~200 B | 依賴清單 |

**總計**：約 150 KB（不含依賴套件）

---

## ⚠️ 常見錯誤

### 錯誤 1：不小心上傳 .env
**後果**：API 金鑰洩漏  
**解決**：
1. 立即更換所有 API 金鑰
2. 從 Git 歷史中移除 .env
```bash
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch .env" \
  --prune-empty --tag-name-filter cat -- --all
```

### 錯誤 2：忘記設定環境變數
**後果**：部署後無法啟動  
**解決**：在 Zeabur 設定環境變數

### 錯誤 3：requirements.txt 不完整
**後果**：部署失敗  
**解決**：確認所有依賴都列在 requirements.txt

---

## 🎯 最終檢查

部署前確認：
- [ ] `.gitignore` 已建立
- [ ] `.env` 不在 Git 追蹤中
- [ ] 備份檔案已刪除
- [ ] `requirements.txt` 完整
- [ ] README.md 已更新
- [ ] 程式碼中沒有敏感資訊
- [ ] 測試本地運行正常

---

## 📝 快速命令參考

```bash
# 檢查 Git 狀態
git status

# 查看將要提交的檔案
git diff --cached --name-only

# 移除已追蹤的檔案
git rm --cached .env

# 清理 Git 快取
git rm -r --cached .
git add .
git commit -m "Update .gitignore"
```

---

**準備好部署了嗎？** 🚀

記得先在本地測試一切正常，再推送到 GitHub！
