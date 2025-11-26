import requests
import json

def verify_api():
    base_url = "https://www.3c91.com.tw/consumer/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Referer': 'https://www.3c91.com.tw/phonelist.html',
        'X-Requested-With': 'XMLHttpRequest'
    }

    # Test 1: All Brands
    print("Fetching allbrands...")
    try:
        resp = requests.get(base_url + "allbrands", headers=headers)
        print(f"Allbrands Status: {resp.status_code}")
        print(f"Allbrands Data: {resp.text[:200]}")
    except Exception as e:
        print(f"Allbrands Error: {e}")

    # Test 2: Phone List without brand
    print("\nFetching phonelist2 (no brand)...")
    params = {
        "type": "手機",
        "limit": 5
    }
    try:
        resp = requests.get(base_url + "phonelist2", params=params, headers=headers)
        data = resp.json()
        if isinstance(data, dict):
            items = data.get('data', [])
            print(f"Got {len(items)} items.")
            if items:
                print(f"First item: {items[0].get('model')}")
        else:
            print(f"Unexpected data type: {type(data)}")
    except Exception as e:
        print(f"Phonelist Error: {e}")

    # Test 3: Phone List with brand
    print("\nFetching phonelist2 (brand=Apple)...")
    params = {
        "type": "手機",
        "brand": "Apple",
        "limit": 5
    }
    try:
        resp = requests.get(base_url + "phonelist2", params=params, headers=headers)
        data = resp.json()
        if isinstance(data, dict):
            items = data.get('data', [])
            print(f"Got {len(items)} items.")
            if items:
                print(f"First item: {items[0].get('model')}")
                
                # Get details for first item
                mid = items[0].get('id')
                print(f"\nFetching details for ID {mid}...")
                resp_det = requests.get(base_url + f"phonelist/{mid}", headers=headers)
                det_data = resp_det.json()
                print("Detail keys:", list(det_data.keys()))
                print("Deduct keys:", list(det_data.get('deductItems', {}).keys()))
        else:
            print(f"Unexpected data type: {type(data)}")
    except Exception as e:
        print(f"Phonelist Brand Error: {e}")

if __name__ == "__main__":
    verify_api()
