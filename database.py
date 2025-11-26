import sqlite3
import datetime

DB_NAME = 'prices.db'

def init_db():
    """Initialize the database table if it doesn't exist."""
    conn = sqlite3.connect(DB_NAME)
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

def save_prices(data):
    """
    Save a list of price data to the database with the current timestamp.
    data: List of dicts [{'model': '...', 'capacity': '...', 'max_price': '...'}, ...]
    """
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    now = datetime.datetime.now()
    
    for item in data:
        c.execute('''
            INSERT INTO prices (model, capacity, price, scraped_at)
            VALUES (?, ?, ?, ?)
        ''', (item['model'], item['capacity'], item['max_price'], now))
        
    conn.commit()
    conn.close()

def get_last_prices():
    """
    Retrieve the prices from the most recent scrape event in the database.
    Returns a dictionary for O(1) lookup: {(model, capacity): price_string}
    """
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    
    # 1. Find the timestamp of the very last scrape
    c.execute('SELECT MAX(scraped_at) FROM prices')
    row = c.fetchone()
    last_time = row[0] if row else None
    
    if not last_time:
        conn.close()
        return {}
        
    # 2. Get all prices associated with that specific timestamp
    c.execute('SELECT model, capacity, price FROM prices WHERE scraped_at = ?', (last_time,))
    rows = c.fetchall()
    conn.close()
    
    # 3. Convert to dictionary
    result = {}
    for row in rows:
        model, capacity, price = row
        result[(model, capacity)] = price
        
    return result
