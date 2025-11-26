# iPhone Trade-in Price Scraper & Web App

這是一個使用 Python Flask 建立的 Web 應用程式，能夠自動從創宇通訊 (3c91) 網站抓取 iPhone 二手機的最高回收價，並以表格形式呈現。

## 功能

*   **自動抓取**: 透過 API 抓取 iPhone 8 到 iPhone 17 的所有型號回收價。
*   **即時更新**: 每次刷新網頁時都會重新抓取最新數據。
*   **清晰呈現**: 使用簡潔的 HTML 表格顯示型號、容量與價格。

## 安裝與執行

1.  **安裝依賴套件**:
    確保您已安裝 Python，然後執行以下指令安裝所需套件：
    ```bash
    pip install -r requirements.txt
    ```

2.  **執行應用程式**:
    ```bash
    python app.py
    ```

3.  **瀏覽網頁**:
    打開瀏覽器並訪問 `http://127.0.0.1:5000/`。

## 專案結構

*   `app.py`: Flask 應用程式主程式。
*   `scraper.py`: 負責抓取與解析數據的邏輯模組。
*   `templates/index.html`: 網頁前端模板。
*   `requirements.txt`: 專案依賴列表。

## 注意事項

*   本程式僅供學習與研究使用。
*   抓取速度取決於目標網站的回應速度。
