# 中古機報價系統 (Quote App)

這是一個使用 Python Flask 建立的 Web 應用程式，能夠自動從創宇通訊 (3c91) 網站抓取 iPhone/Android 二手機的最高回收價，並生成報價單。

## 🌐 線上服務

- **生產環境**：https://quote-app-1037916805822.asia-east1.run.app
- **GCP 專案**：`mobileerpsystem`
- **GitHub 倉庫**：https://github.com/timhuang1006/PRICESYSTEM

---

## 🚀 快速部署（改版時使用）

```bash
gcloud run deploy quote-app \
    --source . \
    --region asia-east1 \
    --execution-environment gen2 \
    --add-volume=name=data-volume,type=cloud-storage,bucket=quote-app-data \
    --add-volume-mount=volume=data-volume,mount-path=/app/data
```

---

## 📋 Google Cloud Console 連結

### Cloud Run 服務管理
https://console.cloud.google.com/run?project=mobileerpsystem

### Cloud Storage 資料管理
https://console.cloud.google.com/storage/browser?project=mobileerpsystem

查看 `quote-app-data` 儲存桶內容（報價單、設定檔等）

### 應用程式日誌
https://console.cloud.google.com/logs/query?project=mobileerpsystem

---

## 📦 功能特色

- ✅ **自動抓取價格**：從 3c91 網站抓取 iPhone/Android 回收價
- ✅ **報價單管理**：生成、編輯、刪除客戶報價單
- ✅ **資料持久化**：使用 GCS Volume Mount，資料永久保存
- ✅ **PDF 匯出**：將報價單匯出為 PDF
- ✅ **LINE 分享**：一鍵分享報價單到 LINE
- ✅ **安全登入**：密碼保護的管理介面
- ✅ **管理後台加密**：隨機生成的管理路徑

---

## 💻 本地開發

### 1. 安裝依賴套件

```bash
pip install -r requirements.txt
```

### 2. 執行應用程式

```bash
python app.py
```

### 3. 瀏覽網頁

打開瀏覽器訪問 `http://127.0.0.1:8080/`

---

## 📂 專案結構

```
├── app.py                  # Flask 主程式
├── scraper.py             # 價格爬蟲模組
├── database.py            # 資料庫操作（已棄用）
├── utils.py               # 工具函數
├── requirements.txt       # Python 依賴
├── Dockerfile             # Docker 容器配置
├── .gitignore            # Git 忽略規則
├── templates/            # HTML 模板
│   ├── index.html        # 主介面
│   ├── login.html        # 登入頁面
│   ├── admin_dashboard.html  # 管理後台
│   └── static_quote.html # 靜態報價單
├── data/                 # 資料目錄（掛載到 GCS）
│   ├── static_quotes/    # 報價單檔案
│   ├── cache/            # 價格快取
│   ├── mappings.json     # 客戶名稱對照表
│   └── admin_config.json # 管理後台設定
└── static_quotes/        # 舊版報價單（已棄用）
```

---

## 🔧 Git 版本控制

### 提交更新

```bash
git add .
git commit -m "描述更新內容"
git push
```

### 查看狀態

```bash
git status
```

### 查看提交歷史

```bash
git log --oneline
```

---

## 🔐 環境變數

應用程式使用以下環境變數：

- `PORT`: 服務埠號（預設 8080，Cloud Run 自動設定）
- `ADMIN_PASSWORD`: 管理員密碼（目前為 `Asdfg11234`）

---

## 📊 資料持久化

本專案使用 **Google Cloud Storage Volume Mount** 確保資料永久保存：

- **儲存桶名稱**：`quote-app-data`
- **掛載路徑**：`/app/data`
- **儲存內容**：
  - 報價單（`static_quotes/`）
  - 價格快取（`cache/`）
  - 客戶對照表（`mappings.json`）
  - 管理後台路徑（`admin_config.json`）

即使重新部署，所有資料都會保留。

---

## 🛠️ 故障排除

### 問題：部署後資料遺失
**解決**：確保部署指令包含 `--add-volume` 和 `--add-volume-mount` 參數

### 問題：無法訪問管理後台
**解決**：檢查日誌中的管理後台路徑，或在首頁登入後使用 `admintim` 指令

### 問題：價格未更新
**解決**：在管理介面點擊「手動刷新」或等待每日凌晨 4 點自動刷新

---

## 📝 注意事項

- 本程式僅供內部使用
- 抓取速度取決於目標網站的回應速度
- 敏感檔案（`service_account.json`、`prices.db`）已加入 `.gitignore`
- 請勿將管理員密碼提交到 Git

---

## 📞 技術支援

如有問題，請聯絡系統管理員或查看：
- [部署指南](https://github.com/timhuang1006/PRICESYSTEM)
- [GCP Console](https://console.cloud.google.com/run?project=mobileerpsystem)

