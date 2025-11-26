"""
完整測試套件運行器
執行所有測試並生成 HTML 報告
"""
import unittest
import sys
import os
import time
import json
from datetime import datetime
from io import StringIO

# 測試結果收集器
class TestResults:
    def __init__(self):
        self.results = {
            'unit_tests': {},
            'functional_tests': {},
            'browser_tests': {},
            'summary': {
                'total': 0,
                'passed': 0,
                'failed': 0,
                'errors': 0,
                'skipped': 0,
                'duration': 0
            }
        }
        self.start_time = None
        self.end_time = None
    
    def start(self):
        self.start_time = time.time()
    
    def end(self):
        self.end_time = time.time()
        self.results['summary']['duration'] = self.end_time - self.start_time

def run_unit_tests():
    """執行單元測試"""
    print("\n" + "="*60)
    print("[1/3] 執行單元測試 (Unit Tests)")
    print("="*60)
    
    result = {
        'name': '單元測試',
        'status': 'unknown',
        'output': '',
        'passed': 0,
        'failed': 0,
        'errors': 0,
        'total': 0,
        'duration': 0
    }
    
    try:
        # 導入測試
        from tests.test_full_system import TestUsedPhoneQuoteSystem
        
        # 創建測試套件
        loader = unittest.TestLoader()
        suite = loader.loadTestsFromTestCase(TestUsedPhoneQuoteSystem)
        
        # 運行測試
        stream = StringIO()
        runner = unittest.TextTestRunner(stream=stream, verbosity=2)
        start = time.time()
        test_result = runner.run(suite)
        duration = time.time() - start
        
        # 收集結果
        result['duration'] = duration
        result['total'] = test_result.testsRun
        result['passed'] = test_result.testsRun - len(test_result.failures) - len(test_result.errors)
        result['failed'] = len(test_result.failures)
        result['errors'] = len(test_result.errors)
        result['output'] = stream.getvalue()
        result['status'] = 'passed' if test_result.wasSuccessful() else 'failed'
        
        print(f"\n測試結果: {result['passed']}/{result['total']} 通過")
        print(f"耗時: {duration:.2f} 秒")
        
    except Exception as e:
        result['status'] = 'error'
        result['output'] = str(e)
        print(f"\n[ERROR] 單元測試執行失敗: {e}")
    
    return result

def run_functional_tests():
    """執行功能測試"""
    print("\n" + "="*60)
    print("[2/3] 執行功能測試 (Functional Tests)")
    print("="*60)
    
    results = []
    
    # 測試1: 價格四捨五入
    print("\n[TEST] 價格四捨五入邏輯測試...")
    test1 = {
        'name': '價格四捨五入測試',
        'status': 'unknown',
        'output': '',
        'duration': 0
    }
    
    try:
        import subprocess
        start = time.time()
        proc = subprocess.run(
            [sys.executable, 'test_rounding.py'],
            capture_output=True,
            text=True,
            timeout=10,
            cwd=os.path.dirname(os.path.abspath(__file__))
        )
        test1['duration'] = time.time() - start
        test1['output'] = proc.stdout + proc.stderr
        test1['status'] = 'passed' if proc.returncode == 0 else 'failed'
        print(f"   結果: {'通過' if test1['status'] == 'passed' else '失敗'}")
    except Exception as e:
        test1['status'] = 'error'
        test1['output'] = str(e)
        print(f"   [ERROR] {e}")
    
    results.append(test1)
    
    # 測試2: 資料庫注入防護
    print("\n[TEST] 資料庫注入防護測試...")
    test2 = {
        'name': '資料庫注入防護測試',
        'status': 'unknown',
        'output': '',
        'duration': 0
    }
    
    try:
        start = time.time()
        proc = subprocess.run(
            [sys.executable, 'test_db_injection.py'],
            capture_output=True,
            text=True,
            timeout=10,
            cwd=os.path.dirname(os.path.abspath(__file__))
        )
        test2['duration'] = time.time() - start
        test2['output'] = proc.stdout + proc.stderr
        test2['status'] = 'passed' if proc.returncode == 0 else 'failed'
        print(f"   結果: {'通過' if test2['status'] == 'passed' else '失敗'}")
    except Exception as e:
        test2['status'] = 'error'
        test2['output'] = str(e)
        print(f"   [ERROR] {e}")
    
    results.append(test2)
    
    return results

def run_browser_tests():
    """執行瀏覽器端到端測試"""
    print("\n" + "="*60)
    print("[3/3] 執行瀏覽器端到端測試 (Browser E2E Tests)")
    print("="*60)
    print("注意: 此測試會打開瀏覽器窗口...")
    
    result = {
        'name': '瀏覽器端到端測試',
        'status': 'unknown',
        'output': '',
        'duration': 0
    }
    
    try:
        import subprocess
        start = time.time()
        proc = subprocess.run(
            [sys.executable, 'test_browser_e2e.py'],
            capture_output=True,
            text=True,
            timeout=60,
            cwd=os.path.dirname(os.path.abspath(__file__))
        )
        result['duration'] = time.time() - start
        result['output'] = proc.stdout + proc.stderr
        result['status'] = 'passed' if proc.returncode == 0 else 'failed'
        
        # 檢查輸出中是否有 PASS 標記
        if '[PASS]' in result['output']:
            result['status'] = 'passed'
        elif '[FAIL]' in result['output']:
            result['status'] = 'failed'
            
        print(f"\n測試結果: {'通過' if result['status'] == 'passed' else '失敗'}")
        print(f"耗時: {result['duration']:.2f} 秒")
        
    except subprocess.TimeoutExpired:
        result['status'] = 'timeout'
        result['output'] = '測試超時（超過60秒）'
        print("\n[TIMEOUT] 瀏覽器測試超時")
    except Exception as e:
        result['status'] = 'error'
        result['output'] = str(e)
        print(f"\n[ERROR] 瀏覽器測試執行失敗: {e}")
    
    return result

def generate_html_report(test_results):
    """生成 HTML 測試報告"""
    print("\n" + "="*60)
    print("生成測試報告...")
    print("="*60)
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # 計算總結
    summary = test_results.results['summary']
    unit_test = test_results.results['unit_tests']
    functional_tests = test_results.results['functional_tests']
    browser_test = test_results.results['browser_tests']
    
    # 更新總計
    summary['total'] = unit_test.get('total', 0) + len(functional_tests) + 1
    summary['passed'] = unit_test.get('passed', 0)
    summary['failed'] = unit_test.get('failed', 0)
    summary['errors'] = unit_test.get('errors', 0)
    
    for ft in functional_tests:
        if ft['status'] == 'passed':
            summary['passed'] += 1
        elif ft['status'] == 'failed':
            summary['failed'] += 1
        else:
            summary['errors'] += 1
    
    if browser_test.get('status') == 'passed':
        summary['passed'] += 1
    elif browser_test.get('status') == 'failed':
        summary['failed'] += 1
    else:
        summary['errors'] += 1
    
    pass_rate = (summary['passed'] / summary['total'] * 100) if summary['total'] > 0 else 0
    
    html_content = f"""<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>測試報告 - {timestamp}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            min-height: 100vh;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 12px;
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
        
        .summary-card {{
            background: white;
            padding: 25px;
            border-radius: 8px;
            text-align: center;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            transition: transform 0.2s;
        }}
        
        .summary-card:hover {{
            transform: translateY(-5px);
        }}
        
        .summary-card .number {{
            font-size: 3em;
            font-weight: bold;
            margin: 10px 0;
        }}
        
        .summary-card .label {{
            color: #666;
            font-size: 1.1em;
        }}
        
        .passed .number {{ color: #28a745; }}
        .failed .number {{ color: #dc3545; }}
        .errors .number {{ color: #fd7e14; }}
        .total .number {{ color: #007bff; }}
        .duration .number {{ font-size: 2em; }}
        .pass-rate .number {{ color: #28a745; }}
        
        .section {{
            padding: 40px;
            border-bottom: 1px solid #e9ecef;
        }}
        
        .section:last-child {{
            border-bottom: none;
        }}
        
        .section h2 {{
            color: #333;
            margin-bottom: 25px;
            font-size: 1.8em;
            display: flex;
            align-items: center;
        }}
        
        .section h2::before {{
            content: '';
            display: inline-block;
            width: 5px;
            height: 30px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            margin-right: 15px;
            border-radius: 3px;
        }}
        
        .test-item {{
            background: #f8f9fa;
            padding: 20px;
            margin-bottom: 15px;
            border-radius: 8px;
            border-left: 5px solid #ddd;
        }}
        
        .test-item.passed {{
            border-left-color: #28a745;
        }}
        
        .test-item.failed {{
            border-left-color: #dc3545;
        }}
        
        .test-item.error {{
            border-left-color: #fd7e14;
        }}
        
        .test-item h3 {{
            color: #333;
            margin-bottom: 10px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        
        .status-badge {{
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 0.9em;
            font-weight: bold;
            text-transform: uppercase;
        }}
        
        .status-badge.passed {{
            background: #28a745;
            color: white;
        }}
        
        .status-badge.failed {{
            background: #dc3545;
            color: white;
        }}
        
        .status-badge.error {{
            background: #fd7e14;
            color: white;
        }}
        
        .test-output {{
            background: #2d2d2d;
            color: #f8f8f2;
            padding: 20px;
            border-radius: 5px;
            font-family: 'Courier New', monospace;
            font-size: 0.9em;
            overflow-x: auto;
            margin-top: 15px;
            white-space: pre-wrap;
            max-height: 400px;
            overflow-y: auto;
        }}
        
        .test-stats {{
            display: flex;
            gap: 20px;
            margin-top: 10px;
            font-size: 0.9em;
            color: #666;
        }}
        
        .test-stats span {{
            display: flex;
            align-items: center;
            gap: 5px;
        }}
        
        .footer {{
            background: #2d2d2d;
            color: white;
            padding: 30px;
            text-align: center;
        }}
        
        @media print {{
            body {{
                background: white;
                padding: 0;
            }}
            
            .container {{
                box-shadow: none;
            }}
            
            .test-output {{
                max-height: none;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🧪 測試報告</h1>
            <div class="timestamp">生成時間: {timestamp}</div>
        </div>
        
        <div class="summary">
            <div class="summary-card total">
                <div class="label">總測試數</div>
                <div class="number">{summary['total']}</div>
            </div>
            <div class="summary-card passed">
                <div class="label">通過</div>
                <div class="number">{summary['passed']}</div>
            </div>
            <div class="summary-card failed">
                <div class="label">失敗</div>
                <div class="number">{summary['failed']}</div>
            </div>
            <div class="summary-card errors">
                <div class="label">錯誤</div>
                <div class="number">{summary['errors']}</div>
            </div>
            <div class="summary-card duration">
                <div class="label">總耗時</div>
                <div class="number">{summary['duration']:.1f}s</div>
            </div>
            <div class="summary-card pass-rate">
                <div class="label">通過率</div>
                <div class="number">{pass_rate:.1f}%</div>
            </div>
        </div>
        
        <div class="section">
            <h2>1. 單元測試</h2>
            <div class="test-item {unit_test.get('status', 'unknown')}">
                <h3>
                    <span>{unit_test.get('name', '單元測試')}</span>
                    <span class="status-badge {unit_test.get('status', 'unknown')}">{unit_test.get('status', 'unknown')}</span>
                </h3>
                <div class="test-stats">
                    <span>📊 總計: {unit_test.get('total', 0)}</span>
                    <span>✅ 通過: {unit_test.get('passed', 0)}</span>
                    <span>❌ 失敗: {unit_test.get('failed', 0)}</span>
                    <span>⚠️ 錯誤: {unit_test.get('errors', 0)}</span>
                    <span>⏱️ 耗時: {unit_test.get('duration', 0):.2f}s</span>
                </div>
                <div class="test-output">{unit_test.get('output', '無輸出')}</div>
            </div>
        </div>
        
        <div class="section">
            <h2>2. 功能測試</h2>
"""
    
    for ft in functional_tests:
        html_content += f"""
            <div class="test-item {ft['status']}">
                <h3>
                    <span>{ft['name']}</span>
                    <span class="status-badge {ft['status']}">{ft['status']}</span>
                </h3>
                <div class="test-stats">
                    <span>⏱️ 耗時: {ft['duration']:.2f}s</span>
                </div>
                <div class="test-output">{ft['output']}</div>
            </div>
"""
    
    html_content += f"""
        </div>
        
        <div class="section">
            <h2>3. 瀏覽器端到端測試</h2>
            <div class="test-item {browser_test.get('status', 'unknown')}">
                <h3>
                    <span>{browser_test.get('name', '瀏覽器測試')}</span>
                    <span class="status-badge {browser_test.get('status', 'unknown')}">{browser_test.get('status', 'unknown')}</span>
                </h3>
                <div class="test-stats">
                    <span>⏱️ 耗時: {browser_test.get('duration', 0):.2f}s</span>
                </div>
                <div class="test-output">{browser_test.get('output', '無輸出')}</div>
            </div>
        </div>
        
        <div class="footer">
            <p>中古機報價系統 - 自動化測試報告</p>
            <p style="margin-top: 10px; opacity: 0.7;">Generated by Test Runner v1.0</p>
        </div>
    </div>
</body>
</html>
"""
    
    # 保存報告
    report_filename = f"test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
    with open(report_filename, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"\n✅ 報告已生成: {report_filename}")
    return report_filename

def main():
    """主函數"""
    print("""
==============================================================
                   完整測試套件運行器                        
==============================================================
    """)
    
    # 初始化結果收集器
    test_results = TestResults()
    test_results.start()
    
    # 執行測試
    test_results.results['unit_tests'] = run_unit_tests()
    test_results.results['functional_tests'] = run_functional_tests()
    test_results.results['browser_tests'] = run_browser_tests()
    
    # 結束計時
    test_results.end()
    
    # 生成報告
    report_file = generate_html_report(test_results)
    
    # 顯示摘要
    print("\n" + "="*60)
    print("測試完成!")
    print("="*60)
    summary = test_results.results['summary']
    print(f"總測試數: {summary['total']}")
    print(f"通過: {summary['passed']}")
    print(f"失敗: {summary['failed']}")
    print(f"錯誤: {summary['errors']}")
    print(f"總耗時: {summary['duration']:.2f} 秒")
    print(f"\n📊 測試報告: {os.path.abspath(report_file)}")
    print("="*60)
    
    # 自動打開報告
    try:
        import webbrowser
        webbrowser.open(os.path.abspath(report_file))
        print("\n瀏覽器將自動打開報告...")
    except:
        pass

if __name__ == "__main__":
    main()
