# Zeabur 部署指南 - LexBoost Bar

## ✅ 準備工作（已完成）

- ✅ 程式碼已推送到 GitHub
- ✅ Repository: https://github.com/Juicyhsu/AICowLaw.git
- ✅ requirements.txt 已準備好
- ✅ .gitignore 已設定

---

## 🚀 Zeabur 部署步驟

### 步驟 1：註冊/登入 Zeabur

1. 前往 https://zeabur.com
2. 點擊右上角「Sign in with GitHub」
3. 授權 Zeabur 存取您的 GitHub

### 步驟 2：建立新專案

1. 點擊「Create Project」
2. 選擇 Region：**Taiwan** 或 **Singapore**（速度較快）
3. 輸入專案名稱：`lexboost-bar` 或任何您喜歡的名稱
4. 點擊「Create」

### 步驟 3：新增服務

1. 在專案頁面，點擊「Add Service」
2. 選擇「Git」
3. 選擇您的 GitHub 帳號
4. 選擇 Repository：`AICowLaw`
5. 選擇 Branch：`main`
6. 點擊「Deploy」

### 步驟 4：Zeabur 自動偵測

Zeabur 會自動：
- ✅ 偵測到 Streamlit 應用
- ✅ 讀取 requirements.txt
- ✅ 安裝所有依賴
- ✅ 啟動應用

### 步驟 5：設定環境變數 ⚠️ 重要！

1. 點擊您的服務
2. 進入「Variables」分頁
3. 新增以下環境變數：

```
GEMINI_API_KEY=你的_Gemini_API_Key
AIRTABLE_API_KEY=你的_Airtable_API_Key
AIRTABLE_BASE_ID=你的_Airtable_Base_ID
PINECONE_API_KEY=你的_Pinecone_API_Key
PINECONE_ENVIRONMENT=你的_Pinecone_Environment
```

**如何取得這些值**：
- 從您本地的 `.env` 檔案複製
- 或從各服務的控制台取得

### 步驟 6：重新部署

1. 設定完環境變數後
2. 點擊「Redeploy」
3. 等待 2-3 分鐘

### 步驟 7：取得網址

1. 部署完成後，點擊「Domains」
2. Zeabur 會自動產生一個網址，例如：
   - `lexboost-bar.zeabur.app`
3. 點擊網址即可訪問！

### 步驟 8：（可選）綁定自訂網域

1. 在「Domains」分頁
2. 點擊「Add Domain」
3. 輸入您的網域名稱
4. 按照指示設定 DNS

---

## 🔧 常見問題

### Q1: 部署失敗怎麼辦？

**檢查事項**：
1. 環境變數是否都設定了？
2. API Keys 是否正確？
3. 查看 Logs 找錯誤訊息

**解決方法**：
- 點擊服務 → Logs
- 查看錯誤訊息
- 修正後點擊「Redeploy」

### Q2: 應用很慢或無法訪問？

**原因**：冷啟動
- Zeabur 免費版會在閒置後休眠
- 第一次訪問需要 10-30 秒啟動

**解決方法**：
- 等待啟動完成
- 或升級到付費版（$5/月）保持運行

### Q3: 如何更新程式碼？

**方法 1：自動部署**
1. 推送到 GitHub
2. Zeabur 自動偵測並重新部署

**方法 2：手動部署**
1. 在 Zeabur 點擊「Redeploy」

### Q4: 環境變數在哪裡？

**位置**：
- 服務頁面 → Variables 分頁
- 可以隨時新增/修改
- 修改後需要 Redeploy

---

## 📊 免費額度

Zeabur 免費版：
- ✅ 5GB 流量/月
- ✅ 512MB RAM
- ✅ 適合 10-50 個使用者
- ⚠️ 閒置會休眠

**升級方案**（如需要）：
- Hobby: $5/月
- Pro: $20/月

---

## 🎯 部署檢查清單

- [ ] GitHub 推送成功
- [ ] Zeabur 專案建立
- [ ] 服務部署成功
- [ ] 環境變數設定完成
- [ ] 應用可以訪問
- [ ] 登入功能正常
- [ ] AI 生成功能正常
- [ ] 資料庫連接正常

---

## 🆘 需要幫助？

如果遇到問題：
1. 查看 Zeabur Logs
2. 檢查環境變數
3. 確認 API Keys 有效
4. 聯繫我協助除錯

---

## 🎉 部署成功後

您的應用將可以：
- ✅ 24/7 在線（付費版）
- ✅ HTTPS 加密
- ✅ 自動備份
- ✅ 隨時更新

**下一步**：
1. 分享網址給朋友
2. 收集使用者回饋
3. 持續優化功能

祝您部署順利！🚀
