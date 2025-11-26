import sqlite3
import datetime
import os
import time

# Mock database functions to avoid messing with the real DB file if needed, 
# but we can also just use a test db name.
TEST_DB_NAME = 'test_prices.db'

def init_test_db():
    if os.path.exists(TEST_DB_NAME):
        os.remove(TEST_DB_NAME)
    conn = sqlite3.connect(TEST_DB_NAME)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS prices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            model TEXT,
            capacity TEXT,
            price TEXT,
            scraped_at TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def save_test_prices(data):
    conn = sqlite3.connect(TEST_DB_NAME)
    c = conn.cursor()
    now = datetime.datetime.now()
    for item in data:
        c.execute('''
            INSERT INTO prices (model, capacity, price, scraped_at)
            VALUES (?, ?, ?, ?)
        ''', (item['model'], item['capacity'], item['max_price'], now))
    conn.commit()
    conn.close()

def get_last_test_prices():
    conn = sqlite3.connect(TEST_DB_NAME)
    c = conn.cursor()
    c.execute('SELECT MAX(scraped_at) FROM prices')
    row = c.fetchone()
    last_time = row[0] if row else None
    
    if not last_time:
        conn.close()
        return {}
        
    c.execute('SELECT model, capacity, price FROM prices WHERE scraped_at = ?', (last_time,))
    rows = c.fetchall()
    conn.close()
    
    result = {}
    for row in rows:
        result[(row[0], row[1])] = row[2]
    return result

def parse_price(price_str):
    if not price_str: return 0
    clean = price_str.replace('$', '').replace(',', '').strip()
    try:
        return int(clean)
    except:
        return 0

def run_test():
    print("Initializing Test DB...")
    init_test_db()
    
    # Step 1: Initial State (Empty)
    print("\nStep 1: Check empty DB")
    last = get_last_test_prices()
    assert last == {}, "DB should be empty"
    print("PASS: DB is empty.")

    # Step 2: First Scrape (T1)
    print("\nStep 2: Simulate First Scrape (T1)")
    data_t1 = [
        {'model': 'iPhone 13', 'capacity': '128GB', 'max_price': '$10,000'},
        {'model': 'iPhone 14', 'capacity': '256GB', 'max_price': '$20,000'}
    ]
    # Logic from app.py
    last_prices = get_last_test_prices()
    for item in data_t1:
        key = (item['model'], item['capacity'])
        last_val_str = last_prices.get(key)
        item['diff'] = 0
        if last_val_str:
            curr = parse_price(item['max_price'])
            prev = parse_price(last_val_str)
            item['diff'] = curr - prev
            
    print(f"T1 Diffs: {[i['diff'] for i in data_t1]}")
    assert all(i['diff'] == 0 for i in data_t1), "First scrape should have 0 diff"
    save_test_prices(data_t1)
    print("PASS: First scrape handled correctly.")
    
    time.sleep(1.1) # Ensure timestamp difference

    # Step 3: Second Scrape (T2) - Price Increase
    print("\nStep 3: Simulate Second Scrape (T2) - Price Increase")
    data_t2 = [
        {'model': 'iPhone 13', 'capacity': '128GB', 'max_price': '$11,000'}, # +1000
        {'model': 'iPhone 14', 'capacity': '256GB', 'max_price': '$20,000'}  # 0
    ]
    last_prices = get_last_test_prices()
    for item in data_t2:
        key = (item['model'], item['capacity'])
        last_val_str = last_prices.get(key)
        item['diff'] = 0
        if last_val_str:
            curr = parse_price(item['max_price'])
            prev = parse_price(last_val_str)
            item['diff'] = curr - prev
            
    print(f"T2 Diffs: {[i['diff'] for i in data_t2]}")
    assert data_t2[0]['diff'] == 1000, "iPhone 13 should be +1000"
    assert data_t2[1]['diff'] == 0, "iPhone 14 should be 0"
    save_test_prices(data_t2)
    print("PASS: Price increase detected.")

    time.sleep(1.1)

    # Step 4: Third Scrape (T3) - Price Decrease
    print("\nStep 4: Simulate Third Scrape (T3) - Price Decrease")
    data_t3 = [
        {'model': 'iPhone 13', 'capacity': '128GB', 'max_price': '$9,000'}, # -2000 from last ($11000)
        {'model': 'iPhone 14', 'capacity': '256GB', 'max_price': '$20,000'}
    ]
    last_prices = get_last_test_prices()
    for item in data_t3:
        key = (item['model'], item['capacity'])
        last_val_str = last_prices.get(key)
        item['diff'] = 0
        if last_val_str:
            curr = parse_price(item['max_price'])
            prev = parse_price(last_val_str)
            item['diff'] = curr - prev
            
    print(f"T3 Diffs: {[i['diff'] for i in data_t3]}")
    assert data_t3[0]['diff'] == -2000, "iPhone 13 should be -2000"
    save_test_prices(data_t3)
    print("PASS: Price decrease detected.")

    # Cleanup
    if os.path.exists(TEST_DB_NAME):
        os.remove(TEST_DB_NAME)
    print("\nAll Tests Passed!")

if __name__ == "__main__":
    run_test()
