import sqlite3
import datetime

DB_NAME = 'prices.db'

def inject_fake_history():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    
    # Create table if not exists (in case app hasn't run yet)
    c.execute('''
        CREATE TABLE IF NOT EXISTS prices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            model TEXT,
            capacity TEXT,
            price TEXT,
            scraped_at TIMESTAMP
        )
    ''')
    
    # Insert a fake record for iPhone 16 Pro Max 1TB with a lower price
    # Real price is likely around $38,000 (from previous check)
    # Let's say it was $37,000 yesterday
    
    fake_time = datetime.datetime.now() - datetime.timedelta(days=1)
    
    # We need to match the exact model name and capacity format
    # Based on previous output: "iPhone 16 Pro Max", "1TB"
    
    fake_data = [
        ("iPhone 16 Pro Max", "1TB", "$37,000"), # Should show +1000 (if real is 38000)
        ("iPhone 16 Pro Max", "512GB", "$40,000"), # Should show negative diff (if real is < 40000)
    ]
    
    for model, cap, price in fake_data:
        print(f"Injecting fake history: {model} {cap} {price}")
        c.execute('''
            INSERT INTO prices (model, capacity, price, scraped_at)
            VALUES (?, ?, ?, ?)
        ''', (model, cap, price, fake_time))
        
    conn.commit()
    conn.close()
    print("Injection complete.")

if __name__ == "__main__":
    inject_fake_history()
