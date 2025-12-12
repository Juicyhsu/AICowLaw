# 雲端部署問題修復指南

## 問題總結

您遇到的問題都與**雲端部署的檔案系統特性**有關：

### 問題 1: 時區不同步 ⏰
- **現象**: 本地端和雲端的「今日已複習」數量不同
- **原因**: Zeabur 伺服器使用 UTC 時區，台灣是 UTC+8
- **影響**: 過了台灣時間 12 點，雲端還停留在昨天

### 問題 2: 自訂模板消失 📝
- **現象**: 雲端版沒有自訂複習間隔模板
- **原因**: `review_settings_*.json` 儲存在本地端，雲端沒有這些檔案
- **影響**: 每個使用者的自訂設定無法同步

### 問題 3: 語音生成失敗 🔊
- **現象**: 畫面一直重置、閃爍
- **原因**: Streamlit 的 `st.audio()` 會觸發頁面重新載入
- **影響**: 語音生成後無法正常播放

---

## 解決方案

### 方案 A: 快速修復（推薦）

#### 1. 修復時區問題

在 Zeabur 設定環境變數：
```
TZ=Asia/Taipei
```

**步驟**：
1. 登入 Zeabur Dashboard
2. 選擇您的專案
3. 點擊「Environment Variables」
4. 新增變數：
   - Name: `TZ`
   - Value: `Asia/Taipei`
5. 儲存並重新部署

#### 2. 複習設定改用資料庫（需要修改程式碼）

將 `review_settings_*.json` 改為儲存在 Airtable，這樣本地和雲端會同步。

#### 3. 語音生成改用下載按鈕

不使用 `st.audio()` 自動播放，改為提供下載按鈕。

---

### 方案 B: 完整修復（需要程式碼修改）

需要修改以下檔案：
1. `data_manager.py` - 加入時區處理
2. `review_settings.py` - 改用 Airtable 儲存
3. `app.py` - 修復 TTS 播放邏輯

---

## 詳細說明

### 為什麼會有這些問題？

#### Zeabur 的檔案系統特性

Zeabur（和大多數雲端平台）使用**臨時檔案系統**：

```
本地端:
├── app.py
├── review_settings_九水.json  ✅ 永久儲存
├── user_styles.json            ✅ 永久儲存
└── ai_cache.json               ✅ 永久儲存

雲端 (Zeabur):
├── app.py                      ✅ 從 Git 部署
├── review_settings_九水.json  ❌ 不存在（本地建立的）
├── user_styles.json            ✅ 從 Git 部署
└── ai_cache.json               ❌ 重啟後消失（臨時檔案）
```

**關鍵差異**：
- ✅ **Git 追蹤的檔案**: 會部署到雲端
- ❌ **本地建立的檔案**: 不會同步到雲端
- ⚠️ **雲端建立的檔案**: 重新部署後會消失

---

### 問題 1: 時區詳解

```python
# 本地端 (台灣 UTC+8)
datetime.now()  # 2025-12-13 01:00:00

# 雲端 (Zeabur UTC+0)
datetime.now()  # 2025-12-12 17:00:00  ← 差了 8 小時！
```

**影響**：
- 台灣時間 12/13 凌晨 1 點
- 雲端認為是 12/12 下午 5 點
- 所以「今日已複習」的判斷不同

**解決方法**：
1. 設定 Zeabur 環境變數 `TZ=Asia/Taipei`
2. 或在程式碼中使用 `pytz` 處理時區

---

### 問題 2: 設定檔詳解

```python
# review_settings.py
self.settings_file = f"review_settings_{user_id}.json"
```

這個檔案是在**本地端首次使用時建立**的：
- 本地端：儲存在 `c:\Users\User\Desktop\法烤牛\主程式\`
- 雲端：不存在（因為沒有加入 Git）

**為什麼 `.gitignore` 忽略它？**
```gitignore
review_settings_*.json  # 我們之前加的規則
```

**解決方法**：
1. 將設定儲存到 Airtable（推薦）
2. 或建立預設設定檔並加入 Git

---

### 問題 3: TTS 閃爍詳解

```python
# 目前的程式碼
audio_bytes = asyncio.run(generate_tts_audio(note.get('content', '')))
st.audio(audio_bytes, format='audio/mp3')  # ← 這會觸發頁面重新載入
```

**Streamlit 特性**：
- `st.audio()` 會導致頁面重新渲染
- 在雲端環境下更明顯（網路延遲）
- 造成畫面閃爍

**解決方法**：
```python
# 改用下載按鈕
st.download_button(
    label="📥 下載語音",
    data=audio_bytes,
    file_name=f"{title}.mp3",
    mime="audio/mp3"
)
```

---

## 立即可做的修復

### 1. 設定 Zeabur 時區（5 分鐘）

1. 前往 https://zeabur.com/
2. 登入並選擇專案
3. 點擊「Environment Variables」
4. 新增：`TZ=Asia/Taipei`
5. 重新部署

### 2. 暫時解決方案：使用預設設定

在雲端版本，使用者會自動使用預設的複習間隔設定。

---

## 需要程式碼修改的完整修復

如果您想要完全解決這些問題，需要：

1. **時區修復**: 在 `data_manager.py` 中使用 `pytz`
2. **設定同步**: 將 `review_settings` 改為儲存在 Airtable
3. **TTS 修復**: 改用下載按鈕而非自動播放

是否需要我幫您實作這些修復？

---

## 總結

| 問題 | 原因 | 快速修復 | 完整修復 |
|------|------|---------|---------|
| 時區不同步 | Zeabur 使用 UTC | 設定 `TZ` 環境變數 | 程式碼加入時區處理 |
| 設定不同步 | 檔案只在本地 | 使用預設設定 | 改用 Airtable 儲存 |
| TTS 閃爍 | Streamlit 特性 | 使用下載按鈕 | 改用下載按鈕 |

**建議**：
1. 立即設定 Zeabur 的 `TZ` 環境變數
2. 如果需要自訂設定同步，我可以幫您修改程式碼
3. TTS 功能建議改用下載按鈕（更穩定）
