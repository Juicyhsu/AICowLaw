# 本地測試環境設定指南

## 📋 目錄
- [前置準備](#前置準備)
- [方案選擇](#方案選擇)
- [詳細設定步驟](#詳細設定步驟)
- [常見問題](#常見問題)

---

## 前置準備

### 1. 必要軟體安裝

測試者需要先安裝以下軟體：

- **Python 3.10 或以上**
  - 下載：https://www.python.org/downloads/
  - 安裝時勾選「Add Python to PATH」
  
- **Git**
  - 下載：https://git-scm.com/downloads
  
- **程式碼編輯器**（選擇一個）
  - VS Code：https://code.visualstudio.com/
  - PyCharm：https://www.jetbrains.com/pycharm/

---

## 方案選擇

### 🔄 方案 A：共享您的資料庫（推薦用於團隊測試）

**優點**：
- ✅ 測試者可以看到真實資料
- ✅ 可以測試多使用者功能
- ✅ 設定簡單快速

**缺點**：
- ⚠️ 測試者可以修改您的資料
- ⚠️ 需要分享 API 金鑰

**適用情境**：信任的團隊成員、短期測試

---

### 🆕 方案 B：測試者建立自己的資料庫

**優點**：
- ✅ 完全獨立，不會影響您的資料
- ✅ 測試者可以自由測試
- ✅ 更安全

**缺點**：
- ⚠️ 設定較複雜
- ⚠️ 需要測試者自己申請 API 金鑰

**適用情境**：長期開發、外部測試者

---

## 詳細設定步驟

### 📦 步驟 1：取得專案程式碼

測試者執行以下指令：

```bash
# 1. Clone 專案
git clone https://github.com/Juicyhsu/AICowLaw.git

# 2. 進入專案目錄
cd AICowLaw

# 3. 安裝依賴套件
pip install -r requirements.txt
```

---

### 🔑 步驟 2：設定環境變數

#### 方案 A：使用您的資料庫

**您需要提供給測試者**：

1. 建立一個 `.env.template` 檔案（不包含真實金鑰）
2. 透過**安全方式**（例如：加密訊息、密碼管理工具）提供真實的 `.env` 檔案

**`.env` 檔案內容**（您需要填入真實值）：

```env
# Gemini API（Google AI Studio）
GEMINI_API_KEY=你的_GEMINI_API_KEY

# Pinecone（向量資料庫）
PINECONE_API_KEY=你的_PINECONE_API_KEY
PINECONE_ENVIRONMENT=us-east-1
PINECONE_INDEX_NAME=legal-exam

# Airtable（筆記資料庫）
AIRTABLE_API_KEY=你的_AIRTABLE_API_KEY
AIRTABLE_BASE_ID=你的_AIRTABLE_BASE_ID
AIRTABLE_TABLE_NAME=Notes

# OpenAI（語音轉文字）
OPENAI_API_KEY=你的_OPENAI_API_KEY
```

**測試者操作**：
1. 將收到的 `.env` 檔案放在專案根目錄
2. 確認檔案名稱是 `.env`（不是 `.env.txt`）

---

#### 方案 B：測試者建立自己的資料庫

**測試者需要自行申請以下服務**：

##### 1️⃣ Gemini API（必要）

1. 前往 https://aistudio.google.com/
2. 登入 Google 帳號
3. 點擊「Get API Key」
4. 建立新的 API Key
5. 複製 API Key

##### 2️⃣ Pinecone（必要）

1. 前往 https://www.pinecone.io/
2. 註冊免費帳號
3. 建立新的 Index：
   - Name: `legal-exam`
   - Dimensions: `768`
   - Metric: `cosine`
   - Region: `us-east-1`
4. 取得 API Key

##### 3️⃣ Airtable（必要）

1. 前往 https://airtable.com/
2. 註冊免費帳號
3. 建立新的 Base（資料庫）
4. 建立 Table，命名為 `Notes`
5. 新增以下欄位：

| 欄位名稱 | 類型 | 說明 |
|---------|------|------|
| `user_id` | Single line text | 使用者 ID |
| `title` | Single line text | 筆記標題 |
| `content` | Long text | 筆記內容 |
| `category` | Single select | 科目分類 |
| `tags` | Multiple select | 標籤 |
| `difficulty` | Single select | 難度 |
| `created_at` | Date | 建立時間 |
| `last_reviewed` | Date | 最後複習時間 |
| `next_review` | Date | 下次複習時間 |
| `review_count` | Number | 複習次數 |
| `ease_factor` | Number | 難易度係數 |
| `interval` | Number | 複習間隔 |
| `last_memory_level` | Single line text | 記憶程度 |

6. 取得 API Key：
   - 點擊右上角頭像 → Account
   - 找到「API」區塊
   - 點擊「Generate API key」

7. 取得 Base ID：
   - 在 Base 頁面，網址列會顯示：`https://airtable.com/appXXXXXXXXXXXXXX/...`
   - `appXXXXXXXXXXXXXX` 就是 Base ID

##### 4️⃣ OpenAI（選用，用於語音轉文字）

1. 前往 https://platform.openai.com/
2. 註冊帳號
3. 充值至少 $5（語音轉文字約 $0.006/分鐘）
4. 建立 API Key

**測試者建立 `.env` 檔案**：

在專案根目錄建立 `.env` 檔案，填入自己申請的 API Keys：

```env
# Gemini API
GEMINI_API_KEY=你申請的_GEMINI_KEY

# Pinecone
PINECONE_API_KEY=你申請的_PINECONE_KEY
PINECONE_ENVIRONMENT=us-east-1
PINECONE_INDEX_NAME=legal-exam

# Airtable
AIRTABLE_API_KEY=你申請的_AIRTABLE_KEY
AIRTABLE_BASE_ID=你的_BASE_ID
AIRTABLE_TABLE_NAME=Notes

# OpenAI（選用）
OPENAI_API_KEY=你申請的_OPENAI_KEY
```

---

### 🚀 步驟 3：啟動專案

```bash
# 在專案目錄執行
streamlit run app.py
```

成功啟動後，瀏覽器會自動開啟 `http://localhost:8501`

---

### 👤 步驟 4：登入測試

預設使用者帳號：

| 使用者名稱 | 密碼 |
|-----------|------|
| 九水 | 13134 |
| 使用者A | a |
| 使用者B | b |
| 使用者C | c |
| 使用者D | d |

---

## 🔒 安全建議

### 方案 A：共享資料庫

如果選擇共享您的資料庫，建議：

1. **使用臨時 API Key**
   - Airtable 和 Pinecone 都支援建立多個 API Key
   - 為測試者建立專用的 Key
   - 測試完成後立即刪除

2. **設定唯讀權限**（如果服務支援）
   - Airtable 可以設定 Base 的協作權限
   - 邀請測試者為「唯讀」成員

3. **備份資料**
   - 測試前先備份 Airtable 資料
   - 使用 Airtable 的「Duplicate base」功能

4. **限制測試時間**
   - 約定測試期限
   - 期限後更換 API Key

### 方案 B：獨立資料庫

這是最安全的方式，完全隔離。

---

## 📝 測試清單

測試者應該測試以下功能：

### 基本功能
- [ ] 登入系統（測試不同使用者）
- [ ] 建立筆記（文字輸入）
- [ ] AI 生成筆記（不同風格）
- [ ] 儲存筆記到資料庫

### 進階功能
- [ ] OCR 圖片辨識
- [ ] 語音轉文字（需要 OpenAI API）
- [ ] 心智圖生成
- [ ] 法律體系圖生成

### 複習系統
- [ ] 查看待複習筆記
- [ ] 更新記憶程度
- [ ] 複習間隔設定

### AI 互動
- [ ] 參考書模式
- [ ] 蘇格拉底問答
- [ ] 爭點搶答遊戲

### 搜尋功能
- [ ] 智慧搜尋
- [ ] 科目篩選
- [ ] 相關度評分

### TTS 功能
- [ ] 筆記轉語音
- [ ] 下載語音檔

---

## ❓ 常見問題

### Q1: 執行 `streamlit run app.py` 時出現 `ModuleNotFoundError`

**解決方法**：
```bash
pip install -r requirements.txt
```

### Q2: 出現 `配置錯誤: 缺少 GEMINI_API_KEY`

**解決方法**：
- 確認 `.env` 檔案在專案根目錄
- 確認 `.env` 檔案內容格式正確
- 確認沒有多餘的空格或引號

### Q3: Airtable 連接失敗

**解決方法**：
- 確認 `AIRTABLE_BASE_ID` 格式正確（以 `app` 開頭）
- 確認 Table 名稱是 `Notes`
- 確認 API Key 有效

### Q4: Pinecone 索引不存在

**解決方法**：
- 首次執行時，系統會自動建立索引
- 等待 10 秒讓索引初始化
- 如果仍然失敗，手動在 Pinecone 控制台建立索引

### Q5: 語音轉文字失敗

**解決方法**：
- 確認已安裝 `openai` 套件
- 確認 OpenAI API Key 有效
- 確認帳戶有餘額

### Q6: 本地端和雲端資料不同步

**說明**：
- 如果使用方案 A（共享資料庫），本地和雲端會同步
- 如果使用方案 B（獨立資料庫），本地和雲端是分開的

---

## 📞 技術支援

如果測試過程中遇到問題：

1. 檢查終端機的錯誤訊息
2. 確認 `.env` 設定正確
3. 確認所有依賴套件已安裝
4. 聯繫專案負責人

---

## 🎯 測試完成後

### 方案 A 使用者
1. 刪除本地的 `.env` 檔案
2. 通知專案負責人測試完成
3. 專案負責人刪除臨時 API Key

### 方案 B 使用者
1. 可以保留環境繼續開發
2. 定期更新程式碼：`git pull`

---

**版本**: v1.0  
**更新日期**: 2025-12-13  
**專案**: LexBoost Bar 法考加速
