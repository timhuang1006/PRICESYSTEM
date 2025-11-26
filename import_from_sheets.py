"""
Google Sheets 批量導入報價單腳本

功能：從 Google Sheets 讀取報價數據並批量導入到報價系統

使用方式：
1. 設置 Google Cloud 服務帳號並下載 service_account.json
2. 在 Google Sheets 中授權服務帳號訪問權限
3. 配置下方的參數
4. 執行腳本: python import_from_sheets.py
"""

import os
import json
import requests
from google.oauth2 import service_account
from googleapiclient.discovery import build

# ==================== 配置區 ====================

# Google Sheets 配置
SPREADSHEET_ID = '1aac8_dwyRlgREVMtHokbIFMYybvto50H2wsIclb5_9A'
SHEET_NAME = ''  # 留空使用默認工作表
DATA_RANGE = 'A2:C100'  # 從第2行開始讀取（跳過標題）

# 報價系統配置
QUOTE_SYSTEM_URL = 'https://quote-app-1037916805822.asia-east1.run.app'
# 或本地測試: 'http://localhost:8080'

# 報價單客戶名稱
CLIENT_NAME = '批量導入_2025-11-24'

# 服務帳號金鑰檔案路徑
SERVICE_ACCOUNT_FILE = 'service_account.json'

# ==================== 功能實現 ====================

def get_sheets_service():
    """建立 Google Sheets API 連接"""
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
    
    if not os.path.exists(SERVICE_ACCOUNT_FILE):
        print(f"[錯誤] 找不到服務帳號金鑰檔案 '{SERVICE_ACCOUNT_FILE}'")
        print("\n請按照以下步驟設置：")
        print("1. 前往 https://console.cloud.google.com/")
        print("2. 選擇專案或創建新專案")
        print("3. 啟用 Google Sheets API")
        print("4. 建立服務帳號並下載 JSON 金鑰")
        print(f"5. 將金鑰檔案重命名為 '{SERVICE_ACCOUNT_FILE}' 並放到此目錄")
        return None
    
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES
    )
    service = build('sheets', 'v4', credentials=credentials)
    return service


def read_google_sheets(service):
    """讀取 Google Sheets 數據"""
    try:
        sheet = service.spreadsheets()
        result = sheet.values().get(
            spreadsheetId=SPREADSHEET_ID,
            range=DATA_RANGE
        ).execute()
        
        values = result.get('values', [])
        print(f"[成功] 讀取 {len(values)} 行數據")
        return values
    
    except Exception as e:
        print(f"[錯誤] 讀取 Google Sheets 失敗: {e}")
        print("\n可能的原因：")
        print("1. Sheets ID 錯誤")
        print("2. 工作表名稱錯誤")
        print("3. 服務帳號未被授權訪問此 Sheet")
        print("\n解決方法：")
        print("1. 複製服務帳號郵箱（從 service_account.json 中查看 'client_email'）")
        print("2. 在 Google Sheets 中點擊「共用」")
        print("3. 將服務帳號郵箱添加為「檢視者」")
        return None


def parse_capacity_and_price(capacity_str, price_str):
    """
    解析容量和價格字串
    
    Args:
        capacity_str: 容量字串，如 "32/128/256" 或 "64/256"
        price_str: 價格字串，如 "200" 或 "3000/3400/3700"
    
    Returns:
        list: [(容量, 價格), ...] 例如 [('32GB', '$200'), ('128GB', '$200')]
    """
    if not capacity_str or not price_str:
        return []
    
    # 拆分容量
    capacities = [c.strip() for c in str(capacity_str).split('/')]
    
    # 拆分價格
    prices = [p.strip() for p in str(price_str).split('/')]
    
    # 配對容量和價格
    result = []
    for i, capacity in enumerate(capacities):
        # 如果價格只有一個，所有容量用同一價格
        # 如果價格有多個，按順序對應
        if len(prices) == 1:
            price = prices[0]
        elif i < len(prices):
            price = prices[i]
        else:
            # 如果價格數量少於容量數量，使用最後一個價格
            price = prices[-1]
        
        # 格式化
        capacity_formatted = f"{capacity}GB" if capacity.isdigit() else capacity
        price_formatted = f"${price}" if not price.startswith('$') else price
        
        result.append((capacity_formatted, price_formatted))
    
    return result


def parse_sheet_data(rows):
    """
    解析 Google Sheets 數據
    
    Args:
        rows: Google Sheets API 返回的數據
    
    Returns:
        list: 報價項目列表
    """
    items = []
    
    for row_idx, row in enumerate(rows, start=2):  # 從第2行開始（A2）
        # 確保至少有3列數據
        if len(row) < 3:
            continue
        
        model = row[0].strip() if row[0] else None
        capacity_str = row[1].strip() if len(row) > 1 and row[1] else None
        price_str = row[2].strip() if len(row) > 2 and row[2] else None
        
        # 跳過空行或無效數據
        if not model or not capacity_str or not price_str:
            print(f"[警告] 跳過第 {row_idx} 行：數據不完整 (型號: {model}, 容量: {capacity_str}, 價格: {price_str})")
            continue
        
        # 解析容量和價格
        capacity_price_pairs = parse_capacity_and_price(capacity_str, price_str)
        
        if not capacity_price_pairs:
            print(f"[警告] 跳過第 {row_idx} 行：無法解析容量和價格")
            continue
        
        # 生成每個容量的報價項目
        for capacity, price in capacity_price_pairs:
            item = {
                'brand': 'Apple',
                'model': f'iPhone {model}',
                'capacity': capacity,
                'price': price
            }
            items.append(item)
            print(f"[OK] 第 {row_idx} 行：{item['model']} {capacity} -> {price}")
    
    return items


def create_quote(items, client_name):
    """
    調用報價系統 API 創建報價單
    
    Args:
        items: 報價項目列表
        client_name: 客戶名稱
    
    Returns:
        dict: API 響應
    """
    try:
        url = f"{QUOTE_SYSTEM_URL}/generate_quote"
        payload = {
            'client_name': client_name,
            'items': items
        }
        
        print(f"\n[執行] 正在創建報價單...")
        print(f"   客戶名稱: {client_name}")
        print(f"   項目數量: {len(items)}")
        
        response = requests.post(url, json=payload, timeout=30)
        response.raise_for_status()
        
        result = response.json()
        
        if result.get('success'):
            print(f"[成功] 報價單創建成功！")
            print(f"   報價單網址: {result.get('link')}")
            return result
        else:
            print(f"[錯誤] 報價單創建失敗: {result.get('message')}")
            return None
    
    except requests.exceptions.ConnectionError:
        print(f"[錯誤] 無法連接到報價系統: {QUOTE_SYSTEM_URL}")
        print("   請確認系統是否正在運行")
        return None
    
    except Exception as e:
        print(f"[錯誤] 創建報價單時發生錯誤: {e}")
        return None


def main():
    """主程式"""
    print("=" * 60)
    print("Google Sheets 批量導入報價單")
    print("=" * 60)
    print()
    
    # 1. 連接 Google Sheets API
    print("[步驟 1/3] 連接 Google Sheets API...")
    service = get_sheets_service()
    if not service:
        return
    print()
    
    # 2. 讀取數據
    print("[步驟 2/3] 讀取 Google Sheets 數據...")
    print(f"   Sheets ID: {SPREADSHEET_ID}")
    print(f"   範圍: {DATA_RANGE}")
    print()
    
    rows = read_google_sheets(service)
    if not rows:
        return
    print()
    
    # 3. 解析數據
    print("[步驟 3/3] 解析數據並創建報價單...")
    print()
    items = parse_sheet_data(rows)
    
    if not items:
        print("【錯誤】沒有有效的數據可以導入")
        return
    
    print()
    print(f"【總計】解析出 {len(items)} 個報價項目")
    print()
    
    # 4. 確認是否繼續
    confirm = input("是否繼續創建報價單？(y/n): ").strip().lower()
    if confirm != 'y':
        print("已取消")
        return
    
    # 5. 創建報價單
    result = create_quote(items, CLIENT_NAME)
    
    if result:
        print()
        print("=" * 60)
        print("【成功】導入完成！")
        print("=" * 60)
    else:
        print()
        print("=" * 60)
        print("【失敗】導入失敗")
        print("=" * 60)


if __name__ == '__main__':
    main()
