# Airtable ReviewSettings Table 設定指南

## 目的
將複習間隔設定從本地 JSON 檔案改為儲存在 Airtable，實現本地端和雲端同步。

---

## 步驟 1：在 Airtable 建立 ReviewSettings Table

### 1.1 登入 Airtable
前往 https://airtable.com/ 並登入您的帳號

### 1.2 開啟您的 Base
找到並開啟您用於此專案的 Base（與 Notes Table 相同的 Base）

### 1.3 建立新的 Table
1. 點擊左側的「+」號或「Add a table」
2. 選擇「Start from scratch」
3. 命名為：`ReviewSettings`

### 1.4 設定欄位

刪除預設欄位，並建立以下欄位：

| 欄位名稱 | 類型 | 說明 | 設定 |
|---------|------|------|------|
| `user_id` | Single line text | 使用者 ID | Primary field |
| `settings` | Long text | 設定內容（JSON 格式） | - |

**重要**：
- `user_id` 必須設為 Primary field（第一個欄位）
- `settings` 用來儲存 JSON 格式的設定

---

## 步驟 2：初始化資料（選用）

如果您想要預先建立使用者的設定，可以手動新增記錄：

### 範例記錄

**Record 1:**
- `user_id`: `九水`
- `settings`: 
```json
{
  "intervals": {
    "完全精通": [6, 14, 28, 60, 60],
    "很熟悉": [4, 10, 20, 40, 60],
    "大致記得": [2, 6, 14, 28, 60],
    "有點印象": [2, 4, 8, 16, 30],
    "完全不記得": [2]
  },
  "mode": "標準複習"
}
```

**Record 2-5:**
為其他使用者（使用者A、使用者B、使用者C、使用者D）建立類似的記錄。

**注意**：如果不預先建立，系統會在使用者第一次修改設定時自動建立。

---

## 步驟 3：驗證設定

### 3.1 本地端測試
```bash
streamlit run app.py
```

1. 登入系統
2. 到「複習推薦」頁面
3. 點擊「⚙️ 自訂複習間隔」
4. 修改間隔設定並儲存
5. 重新整理頁面，確認設定有保留

### 3.2 檢查 Airtable
1. 開啟 Airtable Base
2. 查看 `ReviewSettings` Table
3. 應該會看到新增的記錄，包含使用者 ID 和設定 JSON

### 3.3 雲端測試
1. 推送程式碼到 GitHub
2. 等待 Zeabur 部署完成
3. 訪問 https://aicowlaw.zeabur.app/
4. 登入並修改複習間隔設定
5. 確認本地端和雲端的設定同步

---

## 優點

### ✅ 本地和雲端同步
- 在本地端修改設定，雲端也會更新
- 在雲端修改設定，本地端也會更新
- 所有裝置使用相同的設定

### ✅ 多使用者支援
- 每個使用者有獨立的設定
- 不會互相干擾

### ✅ 資料安全
- 設定儲存在雲端
- 不會因為重新部署而遺失

---

## 常見問題

### Q: 如果 ReviewSettings Table 不存在會怎樣？
A: 系統會自動使用預設設定，不會報錯。但無法儲存自訂設定。

### Q: 如何重置為預設設定？
A: 在「複習推薦」頁面，點擊「重置為預設」按鈕。

### Q: 本地端的 review_settings_*.json 檔案還需要嗎？
A: 不需要了！新版本完全使用 Airtable 儲存。

### Q: 如果 Airtable API 失敗會怎樣？
A: 系統會自動使用預設設定，確保功能正常運作。

---

## 遷移現有設定（選用）

如果您已經有本地的 `review_settings_九水.json` 檔案，可以手動遷移：

1. 開啟本地的 JSON 檔案
2. 複製內容
3. 在 Airtable 的 `ReviewSettings` Table 中新增記錄
4. `user_id` 填入 `九水`
5. `settings` 貼上 JSON 內容

---

**設定完成後，複習間隔設定就會在本地和雲端同步了！** ✅
