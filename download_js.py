import requests

def download_js():
    files = [
        "https://www.3c91.com.tw/jsmain/data.js",
        "https://www.3c91.com.tw/jsmain/phonelist.js"
    ]
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    for url in files:
        filename = url.split('/')[-1]
        try:
            response = requests.get(url, headers=headers)
            response.encoding = 'utf-8' # JS is usually UTF-8
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(response.text)
            print(f"Downloaded {filename}")
        except Exception as e:
            print(f"Error downloading {filename}: {e}")

if __name__ == "__main__":
    download_js()
