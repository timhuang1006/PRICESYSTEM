# 🧪 自動化測試系統使用指南

## 📋 概述

這個自動化測試系統能夠：
- ✅ 執行所有單元測試和整合測試
- 📸 自動截圖記錄瀏覽器測試
- 📊 生成精美的 HTML 測試報告
- 🔍 防止修改 A 功能時破壞 B 功能

## 🚀 快速開始

### 1. 安裝依賴

```bash
pip install selenium
```

### 2. 執行測試

#### 方式 1: 執行單元測試（推薦）

```bash
python test_runner.py
```

這將會:
- 🔄 自動執行 `tests/` 目錄下的所有測試
- 📊 生成帶時間戳的 HTML 報告
- ✨ 顯示彩色的測試結果

#### 方式 2: 執行視覺化瀏覽器測試

```bash
# 先啟動應用
python app.py

# 在另一個終端執行測試
python test_browser_visual.py
```

這將會:
- 🌐 自動打開瀏覽器
- 📸 在每個測試步驟截圖
- 💾 保存截圖到 `test_screenshots_YYYYMMDD_HHMMSS/` 目錄

## 📂 測試文件結構

```
中古機報價/
├── test_runner.py              # 測試執行器（生成 HTML 報告）
├── test_browser_visual.py      # 視覺化瀏覽器測試（帶截圖）
├── test_browser_e2e.py        # 端到端瀏覽器測試（原版）
├── tests/                      # 單元測試目錄
│   └── test_full_system.py    # 完整系統測試
└── test_report_*.html         # 測試報告（自動生成）
```

## 🎯 測試涵蓋範圍

### 單元測試 (`tests/test_full_system.py`)
- ✅ 登入/登出功能
- ✅ 管理員後台訪問
- ✅ 創建報價單
- ✅ 檢查報價單存在
- ✅ 更新單筆價格
- ✅ 刪除報價單
- ✅ 靜態頁面渲染
- ✅ 主頁按鈕隱藏檢查

### 瀏覽器測試 (`test_browser_visual.py`)
- 🌐 應用運行檢查
- 🔐 登入流程測試
- 🎨 主頁 UI 元素檢查
- 🚫 PDF/LINE 按鈕隱藏驗證
- 📝 創建報價單流程
- 📱 Android 品牌載入測試

## 📊 測試報告說明

### HTML 報告內容
- 📈 **總覽統計**: 總測試數、通過數、失敗數、錯誤數、跳過數、通過率
- 📊 **進度條**: 視覺化顯示測試通過率
- 📋 **詳細結果**: 每個測試的狀態、錯誤訊息
- ⏱ **執行時間**: 測試開始時間和總耗時

### 報告文件命名
```
test_report_20251126_213000.html
          ^^^^^^^^_^^^^^^
          日期      時間
```

## 🔧 進階使用

### 自定義測試執行

#### 只執行特定測試
```bash
python -m unittest tests.test_full_system.TestUsedPhoneQuoteSystem.test_01_login_logout
```

#### 執行無頭模式瀏覽器測試
修改 `test_browser_visual.py`:
```python
tester = VisualBrowserTest(headless=True)  # 改為 True
```

### 調整測試配置

在 `test_browser_visual.py` 中修改:
```python
APP_URL = "http://127.0.0.1:8080"  # 應用地址
ADMIN_PASSWORD = "Asdfg11234"      # 管理員密碼
```

## 📸 截圖功能

所有瀏覽器測試的截圖會保存在:
```
test_screenshots_YYYYMMDD_HHMMSS/
├── 151030_01_app_running.png
├── 151031_02_login_page.png
├── 151032_02_login_success.png
├── 151033_03_main_page_top.png
└── ...
```

文件命名格式: `時間_測試編號_描述.png`

## 🛠 集成到 CI/CD

### 在 GitHub Actions 中使用

創建 `.github/workflows/test.yml`:
```yaml
name: Run Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Run tests
        run: python test_runner.py
      - name: Upload test report
        uses: actions/upload-artifact@v2
        with:
          name: test-report
          path: test_report_*.html
```

## ⚠️ 注意事項

1. **瀏覽器測試需要應用運行**
   - 先啟動 `python app.py`
   - 再執行瀏覽器測試

2. **Chrome 驅動版本**
   - 確保 ChromeDriver 版本與 Chrome 瀏覽器版本匹配
   - 可使用 `webdriver-manager` 自動管理: 
     ```bash
     pip install webdriver-manager
     ```

3. **測試數據清理**
   - 單元測試使用臨時目錄，會自動清理
   - 瀏覽器測試可能會創建真實的報價單

## 🎨 測試報告樣式

測試報告使用了:
- 🌈 漸變背景和精美卡片設計
- 📊 動畫進度條
- 🎯 狀態標籤 (通過/失敗/錯誤/跳過)
- 📱 響應式設計，支持打印

## 🔄 持續改進

建議每次修改代碼後執行:
```bash
python test_runner.py
```

確保所有測試都通過再提交代碼！

## 📞 問題排查

### 測試卡住
- 檢查應用是否正常運行
- 檢查瀏覽器驅動是否正確安裝
- 嘗試使用無頭模式

### 測試失敗
- 查看生成的 HTML 報告
- 檢查截圖文件夾中的截圖
- 閱讀錯誤訊息中的堆棧追蹤

---

**Happy Testing! 🎉**
