# 🔀 版本管理指南

## 兩個版本說明

本專案提供兩個 Git 分支，對應不同的使用場景：

### 📌 main 分支（本地版本）

**適合場景**：
- ✅ 在自己電腦上使用
- ✅ 想要完全免費
- ✅ 不需要部署到網路

**技術特色**：
- 語音轉文字：本地 Whisper（openai-whisper 套件）
- 完全免費，無需 API 費用
- 需要安裝 ffmpeg
- Docker Image 約 8.6 GB（無法部署）

**環境變數需求**：
```
GEMINI_API_KEY=你的金鑰
PINECONE_API_KEY=你的金鑰
AIRTABLE_API_KEY=你的金鑰
AIRTABLE_BASE_ID=你的BaseID
```

---

### 🚀 deployment 分支（部署版本）

**適合場景**：
- ✅ 需要部署到 Zeabur/Vercel 等雲端平台
- ✅ 多人使用
- ✅ 跨裝置存取

**技術特色**：
- 語音轉文字：OpenAI Whisper API
- 可部署到雲端
- 不需要 ffmpeg
- Docker Image 約 500 MB
- 費用：約 $0.006/分鐘（你的 $5 可用 5-6 個月）

**環境變數需求**：
```
GEMINI_API_KEY=你的金鑰
PINECONE_API_KEY=你的金鑰
AIRTABLE_API_KEY=你的金鑰
AIRTABLE_BASE_ID=你的BaseID
OPENAI_API_KEY=sk-proj-你的金鑰  ← 額外需要
```

---

## 🔄 版本切換方法

### 查看目前分支
```bash
git branch
# * main  ← 星號表示目前所在分支
#   deployment
```

### 切換到本地版本
```bash
git checkout main
```

執行後：
- ✅ 程式碼自動變回本地 Whisper 版本
- ✅ requirements.txt 自動更新
- ✅ 不需要 OPENAI_API_KEY

### 切換到部署版本
```bash
git checkout deployment
```

執行後：
- ✅ 程式碼自動變成 OpenAI API 版本
- ✅ requirements.txt 自動更新
- ✅ 需要設定 OPENAI_API_KEY

---

## 🤔 如何選擇版本？

### 決策流程圖

```
需要部署到網路上嗎？
  ├─ 是 → 使用 deployment 分支
  └─ 否 → 想要完全免費嗎？
        ├─ 是 → 使用 main 分支
        └─ 否 → 兩個都可以
```

### 詳細比較表

| 項目 | main（本地版本）| deployment（部署版本）|
|------|----------------|---------------------|
| **語音轉文字** | 本地 Whisper | OpenAI API |
| **費用** | 完全免費 | $0.006/分鐘 |
| **部署** | ❌ 無法部署 | ✅ 可部署 |
| **ffmpeg** | ⚠️ 需要安裝 | ✅ 不需要 |
| **Docker 大小** | 8.6 GB | 500 MB |
| **OpenAI Key** | ❌ 不需要 | ✅ 需要 |
| **適合場景** | 個人電腦 | 雲端部署 |

---

## 📝 常見問題

### Q1: 切換分支會遺失程式碼嗎？
**A:** 不會！Git 會自動保存兩個版本，切換時只是改變檔案內容。

### Q2: 我可以同時保留兩個版本嗎？
**A:** 可以！兩個分支都在你的電腦上，隨時可以切換。

### Q3: 如果我修改了程式碼，切換分支會怎樣？
**A:** Git 會提示你先提交變更：
```bash
git add .
git commit -m "我的修改"
git checkout deployment  # 然後才能切換
```

### Q4: 部署版本的語音功能費用會很貴嗎？
**A:** 不會！假設每天轉錄 5 分鐘：
- 每月 150 分鐘
- 費用：150 × $0.006 = $0.90/月
- 你的 $5 可以用 5-6 個月

### Q5: 我可以在本地測試部署版本嗎？
**A:** 可以！
```bash
git checkout deployment
# 在 .env 加入 OPENAI_API_KEY
streamlit run app.py
```

---

## 🚀 推薦使用方式

### 方案 A：只用本地版本
```bash
git checkout main
streamlit run app.py
```
**適合**：個人使用，不需要部署

### 方案 B：只用部署版本
```bash
git checkout deployment
# 部署到 Zeabur
```
**適合**：多人使用，需要網路存取

### 方案 C：兩個都用（推薦）
```bash
# 平常在電腦上用本地版本
git checkout main
streamlit run app.py

# 需要部署時切換
git checkout deployment
git push  # 推送到 GitHub，Zeabur 自動部署
```
**適合**：靈活運用，省錢又方便

---

## 📚 相關文件

- [README.md](./README.md) - 專案說明
- [DEPLOYMENT.md](./DEPLOYMENT.md) - 部署指南
- [JS_MIGRATION_PLAN.md](./JS_MIGRATION_PLAN.md) - JavaScript 遷移計畫

---

**有問題？** 查看 README.md 或聯繫開發團隊！
