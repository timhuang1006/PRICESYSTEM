# Google Sheets 批量導入設置指南

## 📋 前置需求

- Python 3.7+
- Google Cloud 帳號
- Google Sheets 編輯權限

---

## 🚀 快速開始（5步驟）

### 步驟 1: 安裝依賴套件

在專案目錄執行：

```powershell
pip install -r requirements_sheets.txt
```

---

### 步驟 2: 設置 Google Cloud 服務帳號

#### 2.1 創建專案並啟用 API

1. 前往 [Google Cloud Console](https://console.cloud.google.com/)
2. 選擇專案 `mobileerpsystem`（或創建新專案）
3. 在搜尋框輸入 "Google Sheets API"
4. 點擊「啟用」

#### 2.2 創建服務帳號

1. 左側選單 → IAM 與管理 → 服務帳號
2. 點擊「建立服務帳號」
3. 填寫：
   - 名稱：`sheets-importer`
   - 說明：`用於批量導入報價單`
4. 點擊「建立並繼續」
5. 角色選擇：**無需設置**（直接下一步）
6. 點擊「完成」

#### 2.3 下載金鑰

1. 找到剛創建的服務帳號
2. 點擊右側「⋮」→「管理金鑰」
3. 點擊「新增金鑰」→「建立新金鑰」
4. 選擇「JSON」格式
5. 下載後將檔案重命名為 `service_account.json`
6. 移動到專案目錄：`c:\Users\Administrator\Desktop\中古機報價\`

---

### 步驟 3: 授權服務帳號訪問 Google Sheets

1. **找到服務帳號郵箱**：
   - 打開 `service_account.json`
   - 複製 `client_email` 的值（形如 `xxx@xxx.iam.gserviceaccount.com`）

2. **在 Google Sheets 中授權**：
   - 打開您的 Google Sheets: https://docs.google.com/spreadsheets/d/1aac8_dwyRlgREVMtHokbIFMYybvto50H2wsIclb5_9A/edit
   - 點擊右上角「共用」按鈕
   - 貼上服務帳號郵箱
   - 權限選擇「檢視者」
   - 點擊「傳送」（取消「通知使用者」）

---

### 步驟 4: 配置導入腳本（可選）

打開 `import_from_sheets.py`，可修改以下配置：

```python
# 報價單客戶名稱
CLIENT_NAME = '批量導入_2025-11-24'

# 報價系統網址（本地測試時可改為 http://localhost:8080）
QUOTE_SYSTEM_URL = 'https://quote-app-1037916805822.asia-east1.run.app'

# 數據讀取範圍（如果您的數據行數更多，可調整）
DATA_RANGE = f'{SHEET_NAME}!A2:C100'
```

---

### 步驟 5: 執行導入

```powershell
cd "c:\Users\Administrator\Desktop\中古機報價"
python import_from_sheets.py
```

**執行流程**：
1. 讀取 Google Sheets 數據
2. 解析型號、容量、價格
3. 顯示預覽並詢問確認
4. 創建報價單
5. 顯示報價單網址

---

## 📊 數據格式說明

### Google Sheets 格式

| 型號 (A列) | 容量 (B列) | 最高收價 (C列) |
|-----------|-----------|--------------|
| 7         | 32/128/256 | 200          |
| 11        | 64/128    | 3000/3400/3700 |

### 解析規則

1. **型號**: 自動加上 "iPhone" 前綴
   - `7` → `iPhone 7`
   - `11 Pro` → `iPhone 11 Pro`

2. **容量**: 用 `/` 分隔多個容量
   - `32/128/256` → `['32GB', '128GB', '256GB']`

3. **價格對應**:
   - 單一價格：所有容量使用相同價格
   - 多個價格：按順序對應容量
   - 價格數量不足：使用最後一個價格

4. **跳過規則**:
   - 空行自動跳過
   - 沒有型號/容量/價格的行跳過

---

## ❓ 常見問題

### Q: 服務帳號郵箱在哪裡找？

**A**: 打開 `service_account.json`，找到 `client_email` 欄位

### Q: 導入失敗怎麼辦？

**A**: 檢查以下項目：
1. 服務帳號是否已授權訪問 Sheets
2. Sheets ID 是否正確
3. 工作表名稱是否正確
4. 報價系統是否正在運行

### Q: 如何本地測試？

**A**: 修改 `QUOTE_SYSTEM_URL = 'http://localhost:8080'` 並先啟動本地服務：
```powershell
python app.py
```

### Q: 可以修改客戶名稱嗎？

**A**: 可以，修改腳本中的 `CLIENT_NAME` 變數

---

## 📝 檔案結構

```
中古機報價/
├── import_from_sheets.py     # 導入腳本
├── service_account.json       # Google Cloud 金鑰（需下載）
├── requirements_sheets.txt    # Python 依賴
└── SHEETS_IMPORT_GUIDE.md    # 本文檔
```

---

## 🎯 後續使用

設置完成後，每次導入只需：

```powershell
python import_from_sheets.py
```

如果 Google Sheets 數據有更新，重新執行即可！
