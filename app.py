import os
import json
import secrets
from datetime import timedelta, datetime
from flask import Flask, render_template, request, redirect, url_for, session, send_from_directory, jsonify, abort
from apscheduler.schedulers.background import BackgroundScheduler
from pytz import timezone

# 假設你的爬蟲程式名為 scraper.py，這裡嘗試導入
try:
    import scraper
except ImportError:
    scraper = None

app = Flask(__name__)

# --- 1. 系統配置 (Security Config) ---
app.secret_key = 'super_secret_key_change_this_in_production'  # 必填，用於 Session
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=30)  # 記住我 30 天
ADMIN_PASSWORD = "Asdfg11234"  # 管理員密碼

# --- 2. 檔案路徑配置 ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
QUOTES_DIR = os.path.join(DATA_DIR, 'static_quotes')
MAPPINGS_FILE = os.path.join(DATA_DIR, 'mappings.json')
CACHE_DIR = os.path.join(DATA_DIR, 'cache')
ANDROID_CACHE_DIR = os.path.join(CACHE_DIR, 'android_cache')
ADMIN_CONFIG_FILE = os.path.join(DATA_DIR, 'admin_config.json')

# 確保目錄存在
for directory in [DATA_DIR, QUOTES_DIR, CACHE_DIR, ANDROID_CACHE_DIR]:
    if not os.path.exists(directory):
        os.makedirs(directory)

# --- 3. 管理後台路徑加密 ---
def get_or_create_admin_path():
    """取得或創建隨機管理後台路徑"""
    if os.path.exists(ADMIN_CONFIG_FILE):
        with open(ADMIN_CONFIG_FILE, 'r') as f:
            config = json.load(f)
            return config.get('admin_path')
    
    # 生成隨機路徑
    admin_path = f"admin_{secrets.token_hex(4)}"
    with open(ADMIN_CONFIG_FILE, 'w') as f:
        json.dump({'admin_path': admin_path}, f)
    return admin_path

ADMIN_PATH = get_or_create_admin_path()
print(f"管理後台路徑: /{ADMIN_PATH}")

# --- 4. 輔助函式 (Helpers) ---

def load_mappings():
    """讀取名稱與亂碼 ID 的對照表"""
    if os.path.exists(MAPPINGS_FILE):
        try:
            with open(MAPPINGS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError:
            return {}
    return {}

def save_mappings(data):
    """儲存對照表"""
    with open(MAPPINGS_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def get_or_create_id(client_name):
    """取得現有 ID 或生成新 ID (網址加密用)"""
    mappings = load_mappings()
    if client_name in mappings:
        return mappings[client_name]
    
    new_id = secrets.token_hex(4)
    mappings[client_name] = new_id
    save_mappings(mappings)
    return new_id

# --- 5. 快取管理函數 ---
def load_cached_data(data_type='iphone'):
    """從快取載入資料"""
    cache_file = os.path.join(CACHE_DIR, f'{data_type}_data.json')
    if os.path.exists(cache_file):
        try:
            with open(cache_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return None
    return None

def save_cached_data(data, data_type='iphone'):
    """儲存資料到快取"""
    cache_file = os.path.join(CACHE_DIR, f'{data_type}_data.json')
    with open(cache_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    # 更新最後更新時間
    update_file = os.path.join(CACHE_DIR, 'last_update.json')
    updates = {}
    if os.path.exists(update_file):
        with open(update_file, 'r') as f:
            updates = json.load(f)
    
    updates[data_type] = datetime.now().isoformat()
    with open(update_file, 'w') as f:
        json.dump(updates, f, indent=2)

def load_android_brand_cache(brand):
    """載入 Android 品牌快取"""
    cache_file = os.path.join(ANDROID_CACHE_DIR, f'{brand}.json')
    if not os.path.exists(cache_file):
        return None
    
    # 檢查快取是否過期（1小時）
    file_time = datetime.fromtimestamp(os.path.getmtime(cache_file))
    if (datetime.now() - file_time).total_seconds() > 3600:
        return None
    
    try:
        with open(cache_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return None

def save_android_brand_cache(brand, data):
    """儲存 Android 品牌快取"""
    cache_file = os.path.join(ANDROID_CACHE_DIR, f'{brand}.json')
    with open(cache_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def custom_round(price):
    """自訂價格四捨五入邏輯 (取最接近的0, 500, 700)"""
    round_options = [0, 500, 700]
    base = int(price // 1000) * 1000
    best_price = 0
    min_diff = float('inf')
    
    for i in range(-1, 2):  # -1, 0, 1
        current_base = base + (i * 1000)
        for option in round_options:
            candidate = current_base + option
            if candidate < 0:
                continue
            diff = abs(price - candidate)
            if diff < min_diff:
                min_diff = diff
                best_price = candidate
            elif diff == min_diff:
                best_price = max(best_price, candidate)
    
    return best_price

def refresh_iphone_cache():
    """刷新 iPhone 快取（定時任務調用）"""
    if scraper:
        try:
            print("正在執行定時任務:刷新 iPhone 資料...")
            iphone_data = scraper.scrape_all_iphones()
            save_cached_data(iphone_data, 'iphone')
            print("iPhone 資料刷新完成")
        except Exception as e:
            print(f"iPhone 資料刷新失敗: {e}")

# --- 6. 定時任務 (Scheduler) ---
scheduler = BackgroundScheduler(timezone=timezone('Asia/Taipei'))
scheduler.add_job(refresh_iphone_cache, 'cron', hour=4, minute=0)  # 每天凌晨 4 點執行
scheduler.start()

# --- 7. 路由 (Routes) ---

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        password = request.form.get('password')
        remember = request.form.get('remember')
        
        if password == ADMIN_PASSWORD:
            session.clear()
            session['logged_in'] = True
            if remember:
                session.permanent = True
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error="密碼錯誤")
            
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/')
def index():
    """主控台:從快取載入 iPhone 資料"""
    # 檢查是否已登入
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    iphone_data = load_cached_data('iphone')
    
    if iphone_data is None and scraper:
        print("首次載入,正在抓取 iPhone 資料...")
        iphone_data = scraper.scrape_all_iphones()
        save_cached_data(iphone_data, 'iphone')
    elif iphone_data is None:
        iphone_data = []
    
    android_data = []
    type_param = request.args.get('type', 'iPhone')
    
    # Pre-calculate prices for all items (0% deduction)
    for item in iphone_data:
        if item.get('max_price'):
            try:
                max_price = int(str(item['max_price']).replace('$', '').replace(',', '').strip())
                calculated = custom_round(max_price)
                item['default_price'] = f'${calculated:,}'
            except:
                item['default_price'] = '-'
        else:
            item['default_price'] = '-'
    
    for item in android_data:
        if item.get('max_price'):
            try:
                max_price = int(str(item['max_price']).replace('$', '').replace(',', '').strip())
                calculated = custom_round(max_price)
                item['default_price'] = f'${calculated:,}'
            except:
                item['default_price'] = '-'
        else:
            item['default_price'] = '-'
    
    return render_template('index.html', iphone_data=iphone_data, android_data=android_data, is_admin=True, is_static_quote=False, type=type_param)

@app.route('/api/get_brand_data/<brand>', methods=['GET'])
def get_brand_data(brand):
    """獲取指定 Android 品牌的資料（快取 + 按需抓取）"""
    if not session.get('logged_in'):
        return jsonify({'success': False, 'message': '未登入'}), 401
    
    # 檢查快取
    cached_data = load_android_brand_cache(brand)
    if cached_data:
        # Pre-calculate prices for cached data
        for item in cached_data:
            if item.get('max_price'):
                try:
                    max_price = int(str(item['max_price']).replace('$', '').replace(',', '').strip())
                    calculated = custom_round(max_price)
                    item['default_price'] = f'${calculated:,}'
                except:
                    item['default_price'] = '-'
            else:
                item['default_price'] = '-'
        return jsonify({'success': True, 'data': cached_data, 'from_cache': True})
    
    # 快取不存在或過期,抓取新資料
    if not scraper:
        return jsonify({'success': False, 'message': 'Scraper not available'})
    
    try:
        print(f"正在抓取 {brand} 資料...")
        brand_data = scraper.scrape_models(brand, is_android=True)
        
        # Pre-calculate prices for new data
        for item in brand_data:
            if item.get('max_price'):
                try:
                    max_price = int(str(item['max_price']).replace('$', '').replace(',', '').strip())
                    calculated = custom_round(max_price)
                    item['default_price'] = f'${calculated:,}'
                except:
                    item['default_price'] = '-'
            else:
                item['default_price'] = '-'
        
        save_android_brand_cache(brand, brand_data)
        return jsonify({'success': True, 'data': brand_data, 'from_cache': False})
    except Exception as e:
        print(f"抓取 {brand} 資料失敗: {e}")
        return jsonify({'success': False, 'message': str(e)})

@app.route('/refresh_data')
def refresh_data():
    """手動刷新資料（僅管理員）"""
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    refresh_iphone_cache()
    
    return jsonify({
        'success': True,
        'message': 'iPhone 資料已更新',
        'timestamp': datetime.now().isoformat()
    })

@app.route('/get_admin_path')
def get_admin_path():
    """返回管理後台路徑（用於 admintim 指令）"""
    if not session.get('logged_in'):
        return jsonify({'success': False, 'message': '未登入'}), 401
    return jsonify({'success': True, 'admin_path': ADMIN_PATH})

def save_quote_data(quote_id, data_list, client_name=None):
    """儲存報價單資料並生成靜態 HTML (支援合併)"""
    target_dir = os.path.join(QUOTES_DIR, quote_id)
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
        
    json_path = os.path.join(target_dir, 'data.json')
    
    # 1. 讀取現有資料 (如果存在)
    current_data = []
    if os.path.exists(json_path):
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                current_data = json.load(f)
        except:
            current_data = []
            
    # 2. 合併資料 (Upsert logic)
    # 使用 (model, capacity) 作為唯一鍵
    data_map = {}
    
    # 先放入舊資料
    for item in current_data:
        key = f"{item.get('model')}_{item.get('capacity')}"
        data_map[key] = item
        
    # 再放入新資料 (覆蓋舊的)
    for item in data_list:
        key = f"{item.get('model')}_{item.get('capacity')}"
        data_map[key] = item
        
    # 轉回列表
    merged_list = list(data_map.values())
    
    # 3. 儲存合併後的 JSON
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(merged_list, f, ensure_ascii=False, indent=4)
        
    # 4. 生成靜態 HTML
    # 分類資料以供模板使用
    iphone_data = [item for item in merged_list if not item.get('brand') or item.get('brand') == 'Apple']
    android_data = [item for item in merged_list if item.get('brand') and item.get('brand') != 'Apple']
    
    # Sort Android data by brand
    android_data.sort(key=lambda x: x.get('brand', ''))
    
    html_content = render_template('index.html', 
                                   iphone_data=iphone_data,
                                   android_data=android_data,
                                   is_admin=False, 
                                   is_static_quote=True,
                                   quote_client_name=client_name)
                                   
    with open(os.path.join(target_dir, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(html_content)

@app.route('/generate_quote', methods=['POST'])
def generate_quote():
    """生成/更新報價單"""
    try:
        payload = request.json
        client_name = payload.get('client_name')
        items = payload.get('items', [])

        if not client_name:
            return jsonify({'success': False, 'message': 'Missing client name'})

        quote_id = get_or_create_id(client_name)
        
        # Always save quote data to ensure files are created even if items is empty
        save_quote_data(quote_id, items, client_name)
        
        short_link = f"{request.host_url}q/{quote_id}"
        return jsonify({'success': True, 'link': short_link, 'original_name': client_name})
        
    except Exception as e:
        print(f"Error in generate_quote: {e}")
        return jsonify({'success': False, 'message': f"生成報價單時發生錯誤: {str(e)}"})

@app.route('/update_single_price', methods=['POST'])
def update_single_price():
    """單筆更新"""
    try:
        payload = request.json
        client_name = payload.get('client_name')
        updated_item = payload.get('item')
        
        if not client_name or not updated_item:
            return jsonify({'success': False, 'message': 'Missing client name or item data'})

        mappings = load_mappings()
        quote_id = mappings.get(client_name)
        
        if not quote_id:
            quote_id = get_or_create_id(client_name)
            current_data = []
        else:
            json_path = os.path.join(QUOTES_DIR, quote_id, 'data.json')
            if os.path.exists(json_path):
                with open(json_path, 'r', encoding='utf-8') as f:
                    current_data = json.load(f)
            else:
                current_data = []

        found = False
        target_key = f"{updated_item.get('model')}_{updated_item.get('capacity')}"
        
        for i, item in enumerate(current_data):
            current_key = f"{item.get('model')}_{item.get('capacity')}"
            if current_key == target_key:
                current_data[i] = updated_item
                found = True
                break
        
        if not found:
            current_data.append(updated_item)
            
        save_quote_data(quote_id, current_data, client_name)
        
        short_link = f"{request.host_url}q/{quote_id}"
        return jsonify({'success': True, 'link': short_link})

    except Exception as e:
        print(f"Update Single Price Error: {e}")
        return jsonify({'success': False, 'message': f"單筆更新時發生錯誤: {str(e)}"})

@app.route('/q/<quote_id>')
def serve_short_quote(quote_id):
    """短網址路由"""
    target_dir = os.path.join(QUOTES_DIR, quote_id)
    if os.path.exists(os.path.join(target_dir, 'index.html')):
        return send_from_directory(target_dir, 'index.html')
    else:
        abort(404)

@app.route('/check_quote_exists', methods=['POST'])
def check_quote():
    """查詢報價單是否存在"""
    data = request.json
    name = data.get('name')
    mappings = load_mappings()
    
    if name in mappings:
        quote_id = mappings[name]
        return jsonify({'exists': True, 'link': f"/q/{quote_id}"})
    else:
        return jsonify({'exists': False})

@app.route('/delete_quote', methods=['POST'])
def delete_quote():
    """刪除報價單"""
    try:
        data = request.json
        client_name = data.get('client_name')
        
        if not client_name:
            return jsonify({'success': False, 'message': '缺少客戶名稱'})
        
        mappings = load_mappings()
        quote_id = mappings.get(client_name)
        
        if not quote_id:
            return jsonify({'success': False, 'message': '找不到該報價單'})
        
        import shutil
        target_dir = os.path.join(QUOTES_DIR, quote_id)
        if os.path.exists(target_dir):
            shutil.rmtree(target_dir)
        
        del mappings[client_name]
        save_mappings(mappings)
        
        return jsonify({'success': True, 'message': f'報價單 [{client_name}] 已成功刪除'})
        
    except Exception as e:
        print(f"Delete Quote Error: {e}")
        return jsonify({'success': False, 'message': f'刪除時發生錯誤: {str(e)}'})

@app.route(f'/{ADMIN_PATH}')
def admin_dashboard():
    """管理員後台介面（加密路徑）"""
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    mappings = load_mappings()
    quotes_list = []
    
    for client_name, quote_id in mappings.items():
        quote_dir = os.path.join(QUOTES_DIR, quote_id)
        if os.path.exists(quote_dir):
            json_path = os.path.join(quote_dir, 'data.json')
            item_count = 0
            if os.path.exists(json_path):
                try:
                    with open(json_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        item_count = len(data)
                except:
                    pass
            
            quotes_list.append({
                'client_name': client_name,
                'quote_id': quote_id,
                'item_count': item_count,
                'link': f'/q/{quote_id}'
            })
    
    return render_template('admin_dashboard.html', quotes=quotes_list, admin_path=ADMIN_PATH)

if __name__ == '__main__':
    # Cloud Run 會提供 PORT 環境變數
    port = int(os.environ.get('PORT', 8080))
    # 生產環境不使用 debug 模式
    app.run(debug=False, port=port, host='0.0.0.0')