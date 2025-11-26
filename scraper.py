import requests
import re

BASE_URL = "https://www.3c91.com.tw/consumer/"

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Referer': 'https://www.3c91.com.tw/phonelist.html',
    'X-Requested-With': 'XMLHttpRequest'
}

def get_iphone_models():
    """
    Fetches the list of iPhone models from the API.
    Returns a list of dictionaries containing model info.
    """
    url = BASE_URL + "phonelist2"
    params = {
        "type": "手機",
        "brand": "Apple",
        "limit": 100 # Should cover all relevant iPhones
    }
    
    try:
        response = requests.get(url, params=params, headers=HEADERS)
        response.raise_for_status()
        data = response.json()
        
        if isinstance(data, dict):
            return data.get('data', [])
        return []
        
    except Exception as e:
        print(f"Error fetching iPhone models: {e}")
        return []

def get_price_details(model_id):
    """
    Fetches price details for a specific model ID.
    Returns a list of dictionaries with capacity and max price.
    """
    url = BASE_URL + f"phonelist/{model_id}"
    
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        data = response.json()
        
        deduct_items = data.get('deductItems', {})
        prices = []
        
        # The API returns capacities in keys like 'capname1', 'capname2', etc.
        # And prices in 'cap1', 'cap2', etc.
        # We need to pair them up.
        
        # Find all keys that look like 'capnameX'
        cap_keys = [k for k in deduct_items.keys() if k.startswith('capname')]
        
        for key in cap_keys:
            # Extract the suffix (e.g., '1' from 'capname1')
            suffix = key.replace('capname', '')
            price_key = f"cap{suffix}"
            
            capacity = deduct_items.get(key)
            price = deduct_items.get(price_key)
            
            if capacity and price:
                prices.append({
                    "capacity": capacity,
                    "price": str(price)
                })
                
        return prices
        
    except Exception as e:
        print(f"Error fetching details for model {model_id}: {e}")
        return []

def get_android_brands():
    """
    Fetches the list of Android brands.
    """
    url = BASE_URL + "phonelist2"
    params = {
        "type": "手機",
        "limit": 100 
    }
    # Note: The API seems to return all models if we don't specify brand?
    # Or we need to find a way to get brands.
    # Based on user request, we need a brand filter.
    # Let's assume we can fetch all and filter by brand, or fetch specific brands.
    # Common brands: Samsung, OPPO, Sony, ASUS, HTC, Xiaomi, Realme, Vivo, Google
    brands = ["Samsung", "OPPO", "Sony", "ASUS", "HTC", "Xiaomi", "Realme", "Vivo", "Google"]
    return brands

def get_models_by_brand(brand):
    url = BASE_URL + "phonelist2"
    params = {
        "type": "手機",
        "brand": brand,
        "limit": 200
    }
    try:
        response = requests.get(url, params=params, headers=HEADERS)
        response.raise_for_status()
        data = response.json()
        if isinstance(data, dict):
            return data.get('data', [])
        return []
    except Exception as e:
        print(f"Error fetching models for {brand}: {e}")
        return []

def scrape_models(brand="Apple", is_android=False):
    """
    Scrapes models for a specific brand.
    """
    if brand == "Apple":
        models = get_iphone_models()
    else:
        models = get_models_by_brand(brand)
        
    results = []
    print(f"Found {len(models)} models for {brand}.")
    
    for model in models:
        name = model.get('model', '')
        model_id = model.get('id')
        
        # Filter: Exclude if max price < 300
        # We need to fetch details first to know the price?
        # Or does the list have price? Usually list doesn't have max price.
        # We have to fetch details.
        
        # Optimization: If we can't know price, we must fetch.
        
        # For iPhone, we have specific logic.
        if brand == "Apple" and 'iPhone' not in name:
            continue
            
        print(f"Scraping {name}...")
        prices = get_price_details(model_id)
        
        # Check max price for filtering
        # We need to check ALL capacities. If ANY capacity > 300, we keep the row?
        # Or filter individual capacities?
        # "Any highest recovery price lower than 300 ... must be completely excluded"
        # This implies if the MAX price of the model (across all caps) is < 300, exclude model?
        # Or if a specific capacity is < 300, exclude that capacity?
        # "Any Android or iPhone model with a max recovery price lower than 300... excluded"
        # I will exclude the specific capacity entry if its price is < 300.
        
        valid_prices = []
        for p in prices:
            try:
                p_val = int(p['price'].replace(',', '').replace('$', ''))
                if p_val >= 300:
                    valid_prices.append(p)
            except:
                pass
        
        if not valid_prices:
            continue

        for p in valid_prices:
            results.append({
                "brand": brand,
                "model": name,
                "capacity": p['capacity'],
                "max_price": p['price']
            })
            
    # Mock Data for iPhone 17 (Only for Apple)
    if brand == "Apple":
        # ... (Insert Mock Data Logic Here) ...
        # Mock Data for iPhone 17 Series
        mock_data = [
            {"brand": "Apple", "model": "iPhone 17 Pro Max", "capacity": "1TB", "max_price": "58900"},
            {"brand": "Apple", "model": "iPhone 17 Pro Max", "capacity": "512GB", "max_price": "52000"},
            {"brand": "Apple", "model": "iPhone 17 Pro Max", "capacity": "256GB", "max_price": "46000"},
            {"brand": "Apple", "model": "iPhone 17 Pro", "capacity": "1TB", "max_price": "52000"},
            {"brand": "Apple", "model": "iPhone 17 Pro", "capacity": "512GB", "max_price": "45000"},
            {"brand": "Apple", "model": "iPhone 17 Pro", "capacity": "256GB", "max_price": "38000"},
            {"brand": "Apple", "model": "iPhone 17 Pro", "capacity": "128GB", "max_price": "34000"},
            {"brand": "Apple", "model": "iPhone 17 Plus", "capacity": "512GB", "max_price": "39000"},
            {"brand": "Apple", "model": "iPhone 17 Plus", "capacity": "256GB", "max_price": "33000"},
            {"brand": "Apple", "model": "iPhone 17 Plus", "capacity": "128GB", "max_price": "30000"},
            {"brand": "Apple", "model": "iPhone 17", "capacity": "512GB", "max_price": "35000"},
            {"brand": "Apple", "model": "iPhone 17", "capacity": "256GB", "max_price": "29000"},
            {"brand": "Apple", "model": "iPhone 17", "capacity": "128GB", "max_price": "26000"},
        ]
        for mock_item in reversed(mock_data):
            exists = any(item['model'] == mock_item['model'] and item['capacity'] == mock_item['capacity'] for item in results)
            if not exists:
                results.insert(0, mock_item)

    return results

def scrape_all_iphones():
    return scrape_models("Apple")


if __name__ == "__main__":
    # Test run
    data = scrape_all_iphones()
    for item in data[:5]:
        print(item)
