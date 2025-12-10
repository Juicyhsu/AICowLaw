# JavaScript 版本遷移企劃書

## 📋 專案概述

**目標**：將現有的 Python/Streamlit 法考加速系統遷移至 JavaScript/Next.js，並改用 Notion 作為資料庫

**當前技術棧**：
- 前端：Streamlit (Python)
- 後端：Python
- 資料庫：Airtable
- AI：Gemini API, Pinecone
- 部署：Streamlit Cloud

**目標技術棧**：
- 前端：Next.js 14 + React
- 後端：Next.js API Routes
- 資料庫：Notion API
- AI：Gemini API (JS SDK), Pinecone (JS SDK)
- 部署：Zeabur

---

## 🎯 為什麼要遷移到 JS？

### 優點
✅ **更好的 UI/UX** - React 提供更豐富的互動體驗  
✅ **更快的載入速度** - Next.js SSR/SSG 優化  
✅ **更靈活的部署** - 可部署到 Vercel, Zeabur, Netlify 等  
✅ **更好的 SEO** - 如果需要公開網站  
✅ **統一技術棧** - 前後端都是 JavaScript  

### 挑戰
⚠️ **開發時間** - 需要重寫所有功能  
⚠️ **學習曲線** - 如果不熟悉 React/Next.js  
⚠️ **AI SDK 差異** - 需要適應 JS 版本的 API  

---

## 🗄️ Notion vs Airtable 比較

| 項目 | Notion | Airtable | 建議 |
|------|--------|----------|------|
| **免費額度** | 無限頁面 + 區塊 | 1,200 筆記錄/base | ✅ Notion 更大 |
| **API 易用性** | 較複雜 | 簡單直觀 | ⚠️ Airtable 較易 |
| **查詢速度** | 較慢 | 快速 | ⚠️ Airtable 較快 |
| **資料結構** | 頁面 + 屬性 | 表格 + 欄位 | 看需求 |
| **多使用者** | 支援 | 支援 | ✅ 都支援 |
| **JS SDK** | 官方支援 | 官方支援 | ✅ 都有 |

### Notion 資料庫結構

**Database**: Legal Exam Notes

**Properties**:
- Title (title) - 筆記標題
- User ID (rich_text) - 使用者ID
- Content (rich_text) - 筆記內容
- Category (select) - 科目分類
- Tags (multi_select) - 標籤
- Difficulty (select) - 難度
- Review Count (number) - 複習次數
- Ease Factor (number) - 記憶因子
- Interval (number) - 複習間隔
- Next Review (date) - 下次複習時間
- Last Reviewed (date) - 最後複習時間
- Created Time (created_time) - 建立時間

**結論**：✅ **建議使用 Notion**
- 免費額度更大（無限頁面）
- 適合個人/小團隊使用
- API 雖較複雜但功能完整

---

## 🏗️ 技術架構設計

### 前端架構
```
Next.js 14 (App Router)
├── app/
│   ├── (auth)/
│   │   └── login/              # 登入頁面
│   ├── (dashboard)/
│   │   ├── layout.tsx          # 主要佈局
│   │   ├── page.tsx            # 首頁
│   │   ├── notes/              # 筆記管理
│   │   ├── chat/               # AI 問答
│   │   ├── search/             # 搜尋
│   │   └── review/             # 複習
│   ├── api/
│   │   ├── ai/                 # AI API routes
│   │   ├── notes/              # 筆記 API
│   │   └── review/             # 複習 API
│   └── layout.tsx              # 根佈局
├── components/
│   ├── ui/                     # shadcn/ui 組件
│   ├── notes/                  # 筆記相關組件
│   ├── chat/                   # 聊天組件
│   └── review/                 # 複習組件
├── lib/
│   ├── ai/                     # AI 核心邏輯
│   ├── db/                     # Notion 資料庫
│   └── utils/                  # 工具函數
└── types/                      # TypeScript 類型定義
```

### 後端架構
```
API Routes (Next.js)
├── /api/auth/login             # 登入驗證
├── /api/notes
│   ├── GET                     # 取得筆記列表
│   ├── POST                    # 建立筆記
│   ├── PUT                     # 更新筆記
│   └── DELETE                  # 刪除筆記
├── /api/ai
│   ├── /generate               # AI 生成筆記
│   ├── /chat                   # AI 問答
│   └── /quiz                   # 測驗題目生成
├── /api/search                 # 語義搜尋
└── /api/review
    ├── /due                    # 取得到期筆記
    └── /update                 # 更新複習記錄
```

---

## 📦 技術棧詳細規劃

### 核心框架
- **Next.js 14** - React 框架（App Router）
- **TypeScript** - 型別安全
- **Tailwind CSS** - 樣式框架
- **shadcn/ui** - UI 組件庫

### 資料庫 & API
- **@notionhq/client** - Notion 官方 SDK
- **Notion API** - 資料儲存

### AI & 向量搜尋
- **@google/generative-ai** - Gemini JS SDK
- **@pinecone-database/pinecone** - Pinecone JS SDK

### 狀態管理
- **Zustand** - 輕量狀態管理
- **React Query** - 伺服器狀態管理

### 認證
- **NextAuth.js** - 認證系統（可選）
- 或簡單的 Session-based auth

### 部署
- **Zeabur** - 主要部署平台
- **GitHub** - 程式碼託管

---

## 🔄 遷移策略

### 階段一：基礎架構（1-2 週）
- [ ] 建立 Next.js 專案
- [ ] 設定 TypeScript + Tailwind
- [ ] 整合 shadcn/ui
- [ ] 建立基本路由結構
- [ ] 設定環境變數

### 階段二：Notion 整合（1 週）
- [ ] 建立 Notion Database
- [ ] 實作 Notion API 封裝
- [ ] 測試 CRUD 操作
- [ ] 實作資料模型轉換

### 階段三：核心功能（2-3 週）
- [ ] 登入系統
- [ ] 筆記管理（建立/編輯/刪除）
- [ ] AI 筆記生成
- [ ] 搜尋功能（Pinecone 整合）
- [ ] 複習系統（SM-2 演算法）

### 階段四：AI 互動（1-2 週）
- [ ] Gemini API 整合
- [ ] 參考書模式
- [ ] 蘇格拉底模式
- [ ] 爭點搶答遊戲

### 階段五：UI/UX 優化（1 週）
- [ ] 響應式設計
- [ ] 動畫效果
- [ ] 載入狀態
- [ ] 錯誤處理

### 階段六：測試 & 部署（1 週）
- [ ] 功能測試
- [ ] 效能優化
- [ ] Zeabur 部署設定
- [ ] 環境變數配置

**總計時間**：約 7-10 週（全職開發）

---

## 💰 成本估算

### 開發成本
- **開發時間**：7-10 週
- **開發人力**：1 位全端工程師
- **學習成本**：如果不熟悉 Next.js，需額外 1-2 週

### 運營成本（月）
| 服務 | 免費額度 | 付費方案 |
|------|---------|---------|
| Notion | 無限頁面 | $0 |
| Gemini API | 1500 req/day | $0 |
| Pinecone | 10萬向量 | $0 |
| Zeabur | 100 小時/月 | $5-10/月 |

**總計**：免費額度足夠，超過才需付費

---

## 🔧 技術難點分析

### 1. Notion API 複雜度 ⚠️ 中等
**挑戰**：
- 資料結構與 Airtable 不同（頁面 vs 記錄）
- 查詢語法較複雜
- 需要處理 rich text 格式

**解決方案**：
- 建立抽象層封裝 Notion API
- 使用 TypeScript 定義清楚的型別
- 參考官方文件和範例

**預估時間**：1 週

### 2. AI SDK 遷移 ⚠️ 簡單
**挑戰**：
- Python SDK 轉 JS SDK
- API 呼叫方式略有不同

**解決方案**：
- Gemini 和 Pinecone 都有完整的 JS SDK
- API 邏輯相同，只是語法不同

**預估時間**：3-5 天

### 3. 複習演算法 ⚠️ 簡單
**挑戰**：
- SM-2 演算法需要重新實作

**解決方案**：
- 邏輯已經清楚，直接翻譯成 JS
- 可以複用現有的計算邏輯

**預估時間**：2-3 天

### 4. 即時互動 ⚠️ 中等
**挑戰**：
- Streamlit 的即時更新需要改用 React 狀態管理
- AI 回應的串流顯示

**解決方案**：
- 使用 React Query 處理非同步狀態
- 使用 Server-Sent Events (SSE) 實現串流

**預估時間**：1 週

---

## 📝 程式碼範例

### Notion 資料庫操作
```typescript
// lib/db/notion.ts
import { Client } from '@notionhq/client';

const notion = new Client({ auth: process.env.NOTION_API_KEY });
const databaseId = process.env.NOTION_DATABASE_ID!;

export async function createNote(userId: string, data: NoteData) {
  const response = await notion.pages.create({
    parent: { database_id: databaseId },
    properties: {
      Title: { title: [{ text: { content: data.title } }] },
      'User ID': { rich_text: [{ text: { content: userId } }] },
      Content: { rich_text: [{ text: { content: data.content } }] },
      Category: { select: { name: data.category } },
      Difficulty: { select: { name: data.difficulty } },
      // ... 其他屬性
    },
  });
  return response;
}

export async function getNotes(userId: string) {
  const response = await notion.databases.query({
    database_id: databaseId,
    filter: {
      property: 'User ID',
      rich_text: { equals: userId },
    },
  });
  return response.results;
}
```

### AI 生成筆記
```typescript
// lib/ai/gemini.ts
import { GoogleGenerativeAI } from '@google/generative-ai';

const genAI = new GoogleGenerativeAI(process.env.GEMINI_API_KEY!);
const model = genAI.getGenerativeModel({ model: 'gemini-2.5-flash' });

export async function generateNote(content: string, type: string) {
  const prompt = `請將以下法律內容整理成${type}：\n\n${content}`;
  const result = await model.generateContent(prompt);
  return result.response.text();
}
```

### API Route 範例
```typescript
// app/api/notes/route.ts
import { NextRequest, NextResponse } from 'next/server';
import { createNote, getNotes } from '@/lib/db/notion';

export async function GET(request: NextRequest) {
  const userId = request.headers.get('x-user-id');
  if (!userId) return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
  
  const notes = await getNotes(userId);
  return NextResponse.json(notes);
}

export async function POST(request: NextRequest) {
  const userId = request.headers.get('x-user-id');
  if (!userId) return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
  
  const data = await request.json();
  const note = await createNote(userId, data);
  return NextResponse.json(note);
}
```

---

## 🚀 Zeabur 部署設定

### 1. 環境變數
```env
NOTION_API_KEY=secret_xxx
NOTION_DATABASE_ID=xxx
GEMINI_API_KEY=xxx
PINECONE_API_KEY=xxx
NEXTAUTH_SECRET=xxx
NEXTAUTH_URL=https://your-app.zeabur.app
```

### 2. 部署步驟
1. 推送程式碼到 GitHub
2. 連接 Zeabur 到 GitHub Repository
3. 設定環境變數
4. 自動部署

### 3. 成本估算
- 免費額度：100 小時/月
- 超過後：約 $5-10/月

---

## ⚖️ 決策建議

### 應該遷移到 JS 的情況
✅ 需要更好的 UI/UX  
✅ 想要更靈活的部署選項  
✅ 團隊熟悉 JavaScript/React  
✅ 有充足的開發時間（2-3 個月）  
✅ 想要更好的效能和 SEO  

### 可以繼續用 Python 的情況
⚠️ 時間緊迫，需要快速上線  
⚠️ 團隊只熟悉 Python  
⚠️ 當前功能已滿足需求  
⚠️ 不需要複雜的前端互動  

---

## 🎯 建議執行方案

### 方案 A：完全遷移（推薦）
**適合**：有充足時間，想要長期維護

**步驟**：
1. 建立新的 Next.js 專案
2. 逐步遷移功能
3. 並行運行兩個版本
4. 測試完成後切換

**時間**：2-3 個月  
**風險**：中等  
**收益**：高  

### 方案 B：混合架構
**適合**：想要快速改善 UI

**步驟**：
1. 保留 Python 後端
2. 用 Next.js 做前端
3. 透過 API 溝通

**時間**：1-1.5 個月  
**風險**：低  
**收益**：中等  

### 方案 C：保持現狀
**適合**：功能已滿足需求

**步驟**：
1. 優化現有 Streamlit 應用
2. 改善 UI/UX
3. 部署到 Zeabur

**時間**：1-2 週  
**風險**：最低  
**收益**：低  

---

## 📊 風險評估

| 風險 | 可能性 | 影響 | 應對策略 |
|------|--------|------|---------|
| 開發時間超出預期 | 高 | 高 | 分階段開發，先完成核心功能 |
| Notion API 限制 | 中 | 中 | 提前測試 API 限制，準備備案 |
| 資料遷移問題 | 低 | 高 | 建立完整的遷移腳本和測試 |
| 學習曲線陡峭 | 中 | 中 | 提前學習 Next.js 和 Notion API |
| 成本超支 | 低 | 低 | 使用免費額度，監控使用量 |

---

## 🎓 學習資源

### Next.js
- 官方文件：https://nextjs.org/docs
- 教學：https://nextjs.org/learn

### Notion API
- 官方文件：https://developers.notion.com
- JS SDK：https://github.com/makenotion/notion-sdk-js

### Gemini JS SDK
- 文件：https://ai.google.dev/tutorials/node_quickstart

### Pinecone JS SDK
- 文件：https://docs.pinecone.io/docs/node-client

---

## 📋 檢查清單

### 開始前
- [ ] 確認團隊技術能力
- [ ] 評估開發時間
- [ ] 建立 Notion Database
- [ ] 測試 Notion API
- [ ] 學習 Next.js 基礎

### 開發中
- [ ] 建立專案結構
- [ ] 實作核心功能
- [ ] 撰寫測試
- [ ] 優化效能
- [ ] 準備部署

### 部署後
- [ ] 監控錯誤
- [ ] 收集使用者反饋
- [ ] 持續優化
- [ ] 定期備份資料

---

## 💡 最終建議

**建議採用方案 A（完全遷移）**，理由：

1. ✅ **Notion 免費額度更大** - 無限頁面 vs 1,200 筆記錄
2. ✅ **Next.js 生態系統成熟** - 更好的開發體驗
3. ✅ **長期維護性更好** - JavaScript 生態系統活躍
4. ✅ **部署選項更多** - Zeabur, Vercel, Netlify 等

**預估總時間**：2-3 個月（兼職）或 1.5-2 個月（全職）

**預估成本**：免費（使用免費額度）

**風險等級**：中等（可控）

---

**準備好開始了嗎？** 🚀

建議先建立一個小型 POC（概念驗證）測試 Notion API 和 Next.js 整合！
