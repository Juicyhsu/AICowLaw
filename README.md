# 🎓 LexBoost Bar - AI 法律學習助手

> 專為法律考生打造的智慧複習系統，結合 AI 生成、間隔重複記憶法與雲端同步

[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat&logo=Streamlit&logoColor=white)](https://streamlit.io/)
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## ✨ 核心功能

### 📝 AI 智慧生成
- **筆記生成**：輸入主題，AI 自動生成結構化法律筆記
- **心智圖**：視覺化法律概念關聯
- **法律體系圖**：完整法律架構展示
- **語音朗讀**：支援 Edge TTS，隨時隨地聽筆記

### 🔄 智慧複習系統
- **間隔重複演算法**：基於 SM-2，科學安排複習時間
- **自訂複習模板**：
  - 🔥 密集複習（考前衝刺）
  - 📚 標準複習（日常學習）
  - 🌟 輕鬆複習（長期鞏固）
  - ✏️ 自訂模板（完全個人化）
- **熟悉度追蹤**：5 級熟悉度管理
- **複習提醒**：自動計算下次複習時間

### 📊 資料管理
- **雲端同步**：Airtable 雲端儲存
- **向量搜尋**：Pinecone 語義搜尋
- **歷史資料庫**：完整筆記管理與編輯
- **匯出功能**：支援 PDF、Word、Markdown

### 🎨 個人化設定
- **自訂風格**：可調整 UI 配色
- **複習間隔設定**：完全自訂每個熟悉度的間隔序列
- **多模板管理**：新增、編輯、刪除自訂模板

---

## 🚀 快速開始

### 環境需求
- Python 3.8+
- Streamlit
- Google Gemini API
- Airtable API
- Pinecone API

### 安裝步驟

1. **Clone 專案**
```bash
git clone https://github.com/Juicyhsu/AICowLaw.git
cd AICowLaw
```

2. **安裝依賴**
```bash
pip install -r requirements.txt
```

3. **設定環境變數**

建立 `.env` 檔案：
```env
GEMINI_API_KEY=your_gemini_api_key
AIRTABLE_API_KEY=your_airtable_api_key
AIRTABLE_BASE_ID=your_airtable_base_id
PINECONE_API_KEY=your_pinecone_api_key
PINECONE_ENVIRONMENT=your_pinecone_environment
```

4. **啟動應用**
```bash
streamlit run app.py
```

5. **訪問應用**
```
http://localhost:8501
```

---

## 📖 使用指南

### 1. 建立筆記
- 進入「📝 建立筆記」頁面
- 輸入法律主題或上傳 PDF
- AI 自動生成筆記
- 可生成心智圖、法律體系圖
- 支援語音朗讀

### 2. 複習筆記
- 進入「🔄 智慧複習推薦」
- 系統自動推薦今日待複習筆記
- 選擇熟悉度（完全不記得 → 完全精通）
- 系統自動計算下次複習時間

### 3. 自訂複習間隔
- 點擊「⚙️ 複習設定」
- 選擇預設模板或建立自訂模板
- 設定每個熟悉度的間隔序列
- 例如：`1,3,7,14,30,60`（天數）

### 4. 管理筆記
- 進入「📚 歷史資料庫」
- 查看所有筆記
- 編輯、刪除、調整熟悉度
- 查看下次複習時間

---

## 🛠️ 技術架構

### 前端
- **Streamlit**：Web 應用框架
- **自訂 CSS**：個人化 UI 設計

### 後端
- **Google Gemini**：AI 內容生成
- **Airtable**：雲端資料庫
- **Pinecone**：向量搜尋引擎
- **Edge TTS**：文字轉語音

### 核心模組
- `app.py`：主應用程式
- `ai_core.py`：AI 生成邏輯
- `data_manager.py`：資料管理
- `review_settings.py`：複習間隔設定
- `prompt_templates.py`：AI 提示詞模板

---

## 📦 部署

### Zeabur 部署（推薦）

1. 推送到 GitHub
2. 連接 Zeabur 到 GitHub
3. 選擇專案並部署
4. 設定環境變數
5. 完成！

詳細步驟請參考：[ZEABUR_DEPLOYMENT.md](ZEABUR_DEPLOYMENT.md)

### 其他平台
- Google Cloud Platform
- Heroku
- Railway

詳細比較請參考：[DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)

---

## 🎯 複習間隔設定

### 預設模板

**🔥 密集複習**（考前衝刺）
- 完全精通：3 → 7 → 14 → 30 → 60 天
- 很熟悉：2 → 5 → 10 → 20 → 40 天
- 大致記得：1 → 3 → 7 → 14 → 30 天

**📚 標準複習**（日常學習）
- 完全精通：6 → 14 → 28 → 60 → 60 天
- 很熟悉：4 → 10 → 20 → 40 → 60 天
- 大致記得：2 → 6 → 14 → 28 → 60 天

**🌟 輕鬆複習**（長期鞏固）
- 完全精通：7 → 21 → 45 → 60 → 60 天
- 很熟悉：5 → 14 → 30 → 60 → 60 天
- 大致記得：3 → 7 → 14 → 30 → 60 天

### 自訂模板
完全自訂每個熟悉度的間隔序列，長度不限！

---

## 📝 更新日誌

### v2.0.0 (2025-12-12)
- ✨ 新增自訂複習間隔設定功能
- ✨ 支援多個自訂模板管理
- ✨ 新增模板編輯功能
- ✨ 資料庫顯示優化（建立時間、下次複習時間）
- ✨ 複習推薦頁面排序優化
- 🐛 修正語音生成 asyncio 錯誤
- 🐛 修正複習計數器同步問題

### v1.0.0
- 🎉 初始版本發布
- ✨ AI 筆記生成
- ✨ 智慧複習系統
- ✨ 雲端同步
- ✨ 向量搜尋

---

## 🤝 貢獻

歡迎提交 Issue 和 Pull Request！

---

## 📄 授權

MIT License

---

## 👨‍💻 作者

**Juicy Hsu**
- GitHub: [@Juicyhsu](https://github.com/Juicyhsu)

---

## 🙏 致謝

- Google Gemini API
- Streamlit
- Airtable
- Pinecone
- Edge TTS

---

**祝您考試順利！🎓**