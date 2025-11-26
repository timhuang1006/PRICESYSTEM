import os

# 讀取損壞的文件
with open('templates/index.html.broken', 'r', encoding='utf-8') as f:
    broken_content = f.read()

# 創建完整的HTML頭部
html_header = '''<!DOCTYPE html>
<html lang="zh-TW">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>二手機回收價 - {% if type %}{{ type }}{% else %}後台管理{% endif %}</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/html2pdf.js/0.10.1/html2pdf.bundle.min.js"></script>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #f4f4f9;
            margin: 0;
            padding: 20px;
            padding-bottom: 100px;
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }

        h1 {
            text-align: center;
            color: #333;
        }

        .nav-tabs {
            display: flex;
            justify-content: center;
            margin-bottom: 20px;
            border-bottom: 2px solid #ddd;
        }

        .nav-link {
            padding: 10px 20px;
            text-decoration: none;
            color: #555;
            border-bottom: 2px solid transparent;
            margin-bottom: -2px;
            font-weight: bold;
            background: none;
            border: none;
            border-bottom: 2px solid transparent;
            cursor: pointer;
            font-size: 1em;
        }

        .nav-link.active {
            color: #007bff;
            border-bottom-color: #007bff;
        }

        .controls {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
            flex-wrap: wrap;
            gap: 10px;
        }

        .action-group {
            display: flex;
            gap: 10px;
            align-items: center;
        }

        .brand-filters {
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
            margin: 10px 0;
        }

        .brand-btn {
            padding: 8px 16px;
            background: #007bff;
            color: white;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-weight: bold;
        }

        .brand-btn:hover {
            background: #0056b3;
        }

        .brand-btn.active {
            background: #28a745;
        }

        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }

        th,
        td {
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }

        th {
            background-color: #007bff;
            color: white;
        }

        tr:hover {
            background-color: #f1f1f1;
        }

        .price {
            color: #333;
            font-weight: bold;
        }

        .diff-up {
            color: green;
            font-size: 0.9em;
            margin-left: 8px;
        }

        .diff-down {
            color: red;
            font-size: 0.9em;
            margin-left: 8px;
        }

        .final-price-input {
            width: 80px;
            padding: 5px;
        }

        .deduction-input {
            width: 60px;
        }

        .save-btn {
            font-size: 1.2em;
            cursor: pointer;
            border: none;
            background: none;
        }

        #loading-indicator {
            text-align: center;
            padding: 20px;
            font-size: 1.1em;
            color: #007bff;
        }

        .quote-actions {
            display: flex;
            justify-content: center;
            gap: 15px;
            margin: 20px 0;
            padding: 15px;
            background: #f8f9fa;
            border-radius: 8px;
        }

        .action-btn {
            padding: 12px 24px;
            font-size: 16px;
            font-weight: bold;
            border: none;
            border-radius: 6px;
            cursor: pointer;
            transition: all 0.3s ease;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }

        .pdf-btn {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }

        .pdf-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(102, 126, 234, 0.3);
        }

        .line-btn {
            background: linear-gradient(135deg, #06c755 0%, #00b900 100%);
            color: white;
        }

        .line-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(6, 199, 85, 0.3);
        }

        .generation-date-display {
            text-align: center;
            margin: 10px 0;
            font-size: 14px;
            color: #666;
        }

        @media print {
            .quote-actions {
                display: none !important;
            }
        }
    </style>
</head>

<body>
'''

html_footer = '''
</body>

</html>'''

# 組合完整的HTML
full_html = html_header + broken_content + html_footer

# 寫入新文件
with open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(full_html)

print("文件已修復完成！")
