# 🚀 部署指南

## 📋 部署前檢查清單

### 必要條件
- ✅ Gemini API Key (免費)
- ✅ Pinecone API Key (免費)
- ✅ Airtable API Key + Base ID (免費)
- ✅ Python 3.8+

---

## 🗄️ 資料庫說明

### 當前架構：Airtable 雲端資料庫

**為什麼使用 Airtable？**
- ✅ **多使用者支援** - 每個使用者有獨立資料
- ✅ **雲端同步** - 資料儲存在雲端，不會因部署重啟而遺失
- ✅ **免費額度充足** - 1,200 筆記錄/base（個人使用綽綽有餘）
- ✅ **易於管理** - 可直接在 Airtable 網頁查看/編輯資料

**資料儲存位置**：
- 筆記資料 → Airtable (雲端)
- 向量索引 → Pinecone (雲端)
- 無本地資料 → 適合部署到 Streamlit Cloud

---

## 🔑 取得 API 金鑰

### 1. Gemini API (Google AI)
1. 前往 https://makersuite.google.com/app/apikey
2. 登入 Google 帳號
3. 點擊「Create API Key」
4. 複製金鑰

### 2. Pinecone API
1. 前往 https://www.pinecone.io/
2. 註冊免費帳號 (Starter Plan)
3. 進入 Dashboard → API Keys
4. 複製「API Key」

### 3. Airtable API + Base ID

#### 步驟 A：建立 Base
1. 前往 https://airtable.com/
2. 註冊/登入帳號
3. 點擊「Create a base」→「Start from scratch」
4. 命名為「Legal Exam Notes」

#### 步驟 B：建立 Table
1. 在新建的 Base 中，重新命名 Table 為「Notes」
2. 建立以下欄位（Field）：

| 欄位名稱 | 類型 | 說明 |
|---------|------|------|
| user_id | Single line text | 使用者ID |
| title | Single line text | 筆記標題 |
| content | Long text | 筆記內容 |
| category | Single select | 科目分類 |
| tags | Single line text | 標籤（逗號分隔）|
| difficulty | Single select | 難度（簡單/中等/困難）|
| review_count | Number | 複習次數 |
| ease_factor | Number | 記憶因子 |
| interval | Number | 複習間隔（天）|
| next_review | Date | 下次複習時間 |
| last_reviewed | Date | 最後複習時間 |
| created_at | Created time | 建立時間（自動）|

#### 步驟 C：取得 API Key
1. 點擊右上角頭像 → Account
2. 左側選單選擇「Developer hub」
3. 點擊「Create token」
4. 設定權限：
   - Scope: `data.records:read`, `data.records:write`
   - Access: 選擇你剛建立的 Base
5. 點擊「Create token」
6. **複製並保存 API Token**

#### 步驟 D：取得 Base ID
1. 回到你的 Base
2. 點擊「Help」→「API documentation」
3. 在網址列或文件中找到 Base ID
   - 格式：`appXXXXXXXXXXXXXX`
   - 例如：`app1234567890abcd`

---

## 🌐 部署到 Streamlit Cloud（推薦）

### 步驟 1：準備 GitHub Repository
```bash
cd "c:\Users\user\Desktop\法烤牛\主程式"

# 初始化 Git（如果還沒有）
git init

# 建立 .gitignore
echo ".env
__pycache__/
*.pyc
.streamlit/secrets.toml
test.mp3
*.backup*" > .gitignore

# 提交所有檔案
git add .
git commit -m "Initial commit for deployment"

# 推送到 GitHub
git remote add origin https://github.com/你的帳號/legal-exam-ai.git
git branch -M main
git push -u origin main
```

### 步驟 2：部署到 Streamlit Cloud
1. 前往 https://streamlit.io/cloud
2. 使用 GitHub 帳號登入
3. 點擊「New app」
4. 選擇你的 Repository
5. Main file path: `app.py`
6. 點擊「Advanced settings」

### 步驟 3：設定 Secrets（重要！）
在 Secrets 區域輸入：

```toml
GEMINI_API_KEY = "你的_Gemini_API_金鑰"
PINECONE_API_KEY = "你的_Pinecone_API_金鑰"
AIRTABLE_API_KEY = "你的_Airtable_API_金鑰"
AIRTABLE_BASE_ID = "你的_Airtable_Base_ID"
```

### 步驟 4：部署
- 點擊「Deploy!」
- 等待 2-3 分鐘
- 完成！取得網址：`https://你的app名稱.streamlit.app`

---

## 🐛 常見部署問題

### Q1: 部署後顯示「配置錯誤：缺少 XXX_API_KEY」
**A:** 檢查 Streamlit Cloud 的 Secrets 設定是否正確

### Q2: Airtable 連接失敗
**A:** 
1. 確認 API Token 權限包含 `data.records:read` 和 `data.records:write`
2. 確認 Base ID 正確
3. 確認 Table 名稱為「Notes」

### Q3: Pinecone 索引建立失敗
**A:** 
1. 檢查 API Key 是否正確
2. 免費版只能建立 1 個索引，刪除舊的再試
3. 索引名稱改為 `legal-exam-你的名字`

### Q4: 部署後資料會消失嗎？
**A:** 
- ✅ **不會！** 資料儲存在 Airtable 雲端
- ✅ 即使重新部署，資料仍然保留
- ✅ 可以直接在 Airtable 網頁查看資料

---

## 🔒 安全性注意事項

### ⚠️ 絕對不要做的事
- ❌ 不要把 `.env` 檔案推送到 GitHub
- ❌ 不要在程式碼中寫死 API 金鑰
- ❌ 不要分享你的 API 金鑰

### ✅ 應該做的事
- ✅ 使用 `.gitignore` 排除 `.env`
- ✅ 在 Streamlit Cloud 使用 Secrets 管理
- ✅ 定期更換 API 金鑰

---

## 📊 資源限制

### 免費額度
| 服務 | 限制 | 實際使用 |
|------|------|---------|
| Gemini API | 15 req/min, 1500 req/day | 個人使用綽綽有餘 |
| Pinecone | 1 索引, 10萬向量 | 可儲存數千筆記 |
| Airtable | 1,200 records/base | 足夠個人使用 |
| Streamlit Cloud | 1 app | 夠用 |

---

## 🔄 更新部署

### 更新程式碼
```bash
# 修改程式碼後
git add .
git commit -m "Update features"
git push

# Streamlit Cloud 會自動重新部署
```

---

## 🎯 部署檢查清單

部署前確認：
- [ ] 所有 API 金鑰已取得
- [ ] Airtable Base 和 Table 已建立
- [ ] `.gitignore` 已設定
- [ ] `requirements.txt` 完整
- [ ] 程式碼已推送到 GitHub
- [ ] Streamlit Cloud Secrets 已設定
- [ ] 測試登入功能
- [ ] 測試筆記建立
- [ ] 測試搜尋功能

---

**準備好部署了嗎？** 🚀
