import requests
from bs4 import BeautifulSoup
import re

def inspect():
    url = "https://www.3c91.com.tw/phonelist.html"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    try:
        response = requests.get(url, headers=headers)
        response.encoding = response.apparent_encoding # Try to detect encoding
        print(f"Detected Encoding: {response.encoding}")
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Search for "iPhone" in text
        if "iPhone" in response.text:
            print("Found 'iPhone' in raw text.")
        else:
            print("Did NOT find 'iPhone' in raw text.")

        # Check scripts
        scripts = soup.find_all('script')
        print(f"Found {len(scripts)} scripts.")
        for s in scripts:
            if s.get('src'):
                print(f"  Script src: {s.get('src')}")
        
        # Check iframes
        iframes = soup.find_all('iframe')
        print(f"Found {len(iframes)} iframes.")
        for i in iframes:
            print(f"  Iframe src: {i.get('src')}")
            
        # Print all links again with new encoding
        links = soup.find_all('a')
        iphone_links = []
        for link in links:
            href = link.get('href')
            text = link.get_text(strip=True)
            if href and 'iPhone' in text:
                iphone_links.append((text, href))
        
        print(f"Found {len(iphone_links)} iPhone links (after encoding fix).")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    inspect()
