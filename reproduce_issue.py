from flask import Flask, render_template
import os

app = Flask(__name__)

# Mock data to pass to the template
mock_data = [
    {
        "model": "iPhone 13",
        "capacity": "128GB",
        "max_price": "15000",
        "diff": 500
    },
    {
        "model": "iPhone 12",
        "capacity": "64GB",
        "max_price": "10000",
        "diff": -200
    }
]

@app.route('/')
def index():
    return render_template('index.html', data=mock_data)

if __name__ == '__main__':
    # Set template folder to current directory/templates
    # Assuming the script is run from the project root
    print("Attempting to render template...")
    try:
        with app.test_request_context():
            rendered = render_template('index.html', data=mock_data)
            print("Template rendered successfully!")
            print(rendered[:200]) # Print first 200 chars
    except Exception as e:
        print(f"Template rendering failed: {e}")
