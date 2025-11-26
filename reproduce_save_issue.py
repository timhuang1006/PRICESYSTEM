import requests
import time

BASE_URL = "http://localhost:8080"

def test_save_and_generate():
    # 1. Update Price
    print("Updating price for iPhone 17 Pro Max 1TB...")
    payload = {
        "brand": "Apple",
        "model": "iPhone 17 Pro Max",
        "capacity": "1TB",
        "price": "99999"
    }
    try:
        res = requests.post(f"{BASE_URL}/update_price", json=payload)
        print(f"Update response: {res.status_code}, {res.json()}")
    except Exception as e:
        print(f"Failed to update: {e}")
        return

    # 2. Check Main Site
    print("Checking main site...")
    try:
        res = requests.get(f"{BASE_URL}/iphone")
        if "99999" in res.text:
            print("SUCCESS: Main site shows updated price.")
        else:
            print("FAILURE: Main site does NOT show updated price.")
            # print(res.text[:500])
    except Exception as e:
        print(f"Failed to check main site: {e}")

    # 3. Generate Quote
    print("Generating quote 'TestSave'...")
    # Note: The frontend sends the items. If we use the API directly, we are simulating the frontend.
    # If the frontend logic is broken, this test might pass but the user still has issues.
    # But let's verify the backend logic first.
    
    # Simulating what the frontend sends. 
    # The frontend scrapes the DOM. If the DOM has "99999" (which we verified in step 2 if we refreshed),
    # then it sends "99999".
    
    items = [
        {"brand": "Apple", "model": "iPhone 17 Pro Max", "capacity": "1TB", "final_price": "99999"}
    ]
    gen_payload = {
        "quote_name": "TestSave",
        "items": items
    }
    
    try:
        res = requests.post(f"{BASE_URL}/generate_quote", json=gen_payload)
        print(f"Generate response: {res.status_code}, {res.json()}")
    except Exception as e:
        print(f"Failed to generate: {e}")

    # 4. Check Static Site
    print("Checking static site...")
    try:
        res = requests.get(f"{BASE_URL}/static_quotes/TestSave/index.html")
        if "99999" in res.text:
            print("SUCCESS: Static site shows updated price.")
        else:
            print("FAILURE: Static site does NOT show updated price.")
    except Exception as e:
        print(f"Failed to check static site: {e}")

if __name__ == "__main__":
    test_save_and_generate()
