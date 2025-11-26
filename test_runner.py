"""
自動化測試執行器 - 視覺化測試報告
運行所有測試並生成 HTML 報告
"""
import unittest
import sys
import os
from datetime import datetime
from io import StringIO
import json
import html

class ColoredTextTestResult(unittest.TextTestResult):
    """帶顏色的測試結果輸出"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.test_results = []
        
    def addSuccess(self, test):
        super().addSuccess(test)
        self.test_results.append({
            'name': str(test),
            'status': 'PASS',
            'message': '',
            'time': 0
        })
        print(f"✓ {test} ... PASS")
        
    def addError(self, test, err):
        super().addError(test, err)
        self.test_results.append({
            'name': str(test),
            'status': 'ERROR',
            'message': self._exc_info_to_string(err, test),
            'time': 0
        })
        print(f"✗ {test} ... ERROR")
        
    def addFailure(self, test, err):
        super().addFailure(test, err)
        self.test_results.append({
            'name': str(test),
            'status': 'FAIL',
            'message': self._exc_info_to_string(err, test),
            'time': 0
        })
        print(f"✗ {test} ... FAIL")
        
    def addSkip(self, test, reason):
        super().addSkip(test, reason)
        self.test_results.append({
            'name': str(test),
            'status': 'SKIP',
            'message': reason,
            'time': 0
        })
        print(f"⊘ {test} ... SKIP ({reason})")

class HTMLTestReport:
    """生成 HTML 測試報告"""
    
    def __init__(self, result, start_time, end_time):
        self.result = result
        self.start_time = start_time
        self.end_time = end_time
        self.duration = (end_time - start_time).total_seconds()
        
    def generate(self, filename='test_report.html'):
        """生成 HTML 報告"""
        total = self.result.testsRun
        passed = total - len(self.result.failures) - len(self.result.errors) - len(self.result.skipped)
        failed = len(self.result.failures)
        errors = len(self.result.errors)
        skipped = len(self.result.skipped)
        
        pass_rate = (passed / total * 100) if total > 0 else 0
        
        html_content = f"""<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>測試報告 - {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', 'Microsoft JhengHei', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
        }}
        
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }}
        
        .header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        }}
        
        .header .timestamp {{
            font-size: 1.1em;
            opacity: 0.9;
        }}
        
        .summary {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            padding: 40px;
            background: #f8f9fa;
        }}
        
        .stat-card {{
            background: white;
            padding: 25px;
            border-radius: 15px;
            text-align: center;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            transition: transform 0.3s ease;
        }}
        
        .stat-card:hover {{
            transform: translateY(-5px);
        }}
        
        .stat-card .number {{
            font-size: 3em;
            font-weight: bold;
            margin-bottom: 10px;
        }}
        
        .stat-card .label {{
            font-size: 1.1em;
            color: #666;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}
        
        .stat-card.total .number {{ color: #6c757d; }}
        .stat-card.passed .number {{ color: #28a745; }}
        .stat-card.failed .number {{ color: #dc3545; }}
        .stat-card.errors .number {{ color: #fd7e14; }}
        .stat-card.skipped .number {{ color: #6c757d; }}
        .stat-card.rate .number {{ color: #007bff; }}
        
        .progress-bar {{
            margin: 20px 40px;
            height: 30px;
            background: #e9ecef;
            border-radius: 15px;
            overflow: hidden;
            box-shadow: inset 0 2px 4px rgba(0,0,0,0.1);
        }}
        
        .progress-fill {{
            height: 100%;
            background: linear-gradient(90deg, #28a745 0%, #20c997 100%);
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-weight: bold;
            transition: width 1s ease;
        }}
        
        .test-results {{
            padding: 40px;
        }}
        
        .test-results h2 {{
            font-size: 2em;
            margin-bottom: 30px;
            color: #333;
            border-bottom: 3px solid #667eea;
            padding-bottom: 10px;
        }}
        
        .test-item {{
            background: white;
            border: 1px solid #dee2e6;
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 15px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.05);
            transition: all 0.3s ease;
        }}
        
        .test-item:hover {{
            box-shadow: 0 4px 16px rgba(0,0,0,0.1);
        }}
        
        .test-item.pass {{
            border-left: 5px solid #28a745;
        }}
        
        .test-item.fail {{
            border-left: 5px solid #dc3545;
            background: #fff5f5;
        }}
        
        .test-item.error {{
            border-left: 5px solid #fd7e14;
            background: #fff8f0;
        }}
        
        .test-item.skip {{
            border-left: 5px solid #6c757d;
            background: #f8f9fa;
        }}
        
        .test-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 10px;
        }}
        
        .test-name {{
            font-size: 1.1em;
            font-weight: 600;
            color: #333;
        }}
        
        .test-status {{
            padding: 5px 15px;
            border-radius: 20px;
            font-weight: bold;
            font-size: 0.9em;
        }}
        
        .test-status.pass {{
            background: #28a745;
            color: white;
        }}
        
        .test-status.fail {{
            background: #dc3545;
            color: white;
        }}
        
        .test-status.error {{
            background: #fd7e14;
            color: white;
        }}
        
        .test-status.skip {{
            background: #6c757d;
            color: white;
        }}
        
        .test-message {{
            margin-top: 15px;
            padding: 15px;
            background: #f8f9fa;
            border-radius: 8px;
            font-family: 'Courier New', monospace;
            font-size: 0.9em;
            white-space: pre-wrap;
            word-wrap: break-word;
            color: #dc3545;
        }}
        
        .footer {{
            background: #343a40;
            color: white;
            padding: 20px;
            text-align: center;
        }}
        
        @media print {{
            body {{
                background: white;
            }}
            .container {{
                box-shadow: none;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🧪 自動化測試報告</h1>
            <div class="timestamp">
                執行時間: {self.start_time.strftime('%Y年%m月%d日 %H:%M:%S')} <br>
                耗時: {self.duration:.2f} 秒
            </div>
        </div>
        
        <div class="summary">
            <div class="stat-card total">
                <div class="number">{total}</div>
                <div class="label">總測試數</div>
            </div>
            <div class="stat-card passed">
                <div class="number">{passed}</div>
                <div class="label">通過</div>
            </div>
            <div class="stat-card failed">
                <div class="number">{failed}</div>
                <div class="label">失敗</div>
            </div>
            <div class="stat-card errors">
                <div class="number">{errors}</div>
                <div class="label">錯誤</div>
            </div>
            <div class="stat-card skipped">
                <div class="number">{skipped}</div>
                <div class="label">跳過</div>
            </div>
            <div class="stat-card rate">
                <div class="number">{pass_rate:.1f}%</div>
                <div class="label">通過率</div>
            </div>
        </div>
        
        <div class="progress-bar">
            <div class="progress-fill" style="width: {pass_rate}%;">
                {pass_rate:.1f}% 通過
            </div>
        </div>
        
        <div class="test-results">
            <h2>📋 詳細測試結果</h2>
"""
        
        # Add all test results
        for test_result in self.result.test_results:
            status = test_result['status'].lower()
            status_text = {
                'pass': '✓ 通過',
                'fail': '✗ 失敗',
                'error': '⚠ 錯誤',
                'skip': '⊘ 跳過'
            }.get(status, status)
            
            message_html = ''
            if test_result['message']:
                escaped_message = html.escape(test_result['message'])
                message_html = f'<div class="test-message">{escaped_message}</div>'
            
            html_content += f"""
            <div class="test-item {status}">
                <div class="test-header">
                    <div class="test-name">{html.escape(test_result['name'])}</div>
                    <div class="test-status {status}">{status_text}</div>
                </div>
                {message_html}
            </div>
"""
        
        html_content += """
        </div>
        
        <div class="footer">
            <p>自動化測試系統 | 中古機報價管理系統</p>
        </div>
    </div>
    
    <script>
        // Animate progress bar on load
        window.addEventListener('load', function() {
            const progressBar = document.querySelector('.progress-fill');
            const width = progressBar.style.width;
            progressBar.style.width = '0%';
            setTimeout(() => {
                progressBar.style.width = width;
            }, 100);
        });
    </script>
</body>
</html>
"""
        
        # Save to file
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"\n✓ HTML 測試報告已生成: {filename}")
        return filename

def run_tests():
    """執行所有測試並生成報告"""
    print("="*70)
    print("🧪 啟動自動化測試系統")
    print("="*70)
    print()
    
    # Record start time
    start_time = datetime.now()
    
    # Load tests
    loader = unittest.TestLoader()
    start_dir = 'tests'
    suite = loader.discover(start_dir, pattern='test_*.py')
    
    # Run tests with custom result
    runner = unittest.TextTestRunner(resultclass=ColoredTextTestResult, verbosity=2)
    result = runner.run(suite)
    
    # Record end time
    end_time = datetime.now()
    
    # Generate HTML report
    print()
    print("="*70)
    print("📊 生成測試報告...")
    print("="*70)
    
    report = HTMLTestReport(result, start_time, end_time)
    report_file = report.generate(f'test_report_{start_time.strftime("%Y%m%d_%H%M%S")}.html')
    
    # Print summary
    print()
    print("="*70)
    print("📈 測試摘要")
    print("="*70)
    print(f"總測試數: {result.testsRun}")
    print(f"✓ 通過: {result.testsRun - len(result.failures) - len(result.errors) - len(result.skipped)}")
    print(f"✗ 失敗: {len(result.failures)}")
    print(f"⚠ 錯誤: {len(result.errors)}")
    print(f"⊘ 跳過: {len(result.skipped)}")
    print(f"⏱ 耗時: {(end_time - start_time).total_seconds():.2f} 秒")
    print("="*70)
    
    return result.wasSuccessful()

if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)
