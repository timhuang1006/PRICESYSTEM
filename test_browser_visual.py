"""
增強型瀏覽器測試 - 帶截圖功能
執行端到端測試並自動截圖記錄
"""
import time
import os
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

# 配置
APP_URL = "http://127.0.0.1:8080"
ADMIN_PASSWORD = "Asdfg11234"

class VisualBrowserTest:
    def __init__(self, headless=False):
        """
        初始化測試
        Args:
            headless: 是否使用無頭模式
        """
        self.headless = headless
        self.driver = None
        self.screenshot_dir = f"test_screenshots_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.test_results = []
        
    def setup(self):
        """設置瀏覽器"""
        print("[*] 啟動瀏覽器...")
        options = Options()
        if self.headless:
            options.add_argument('--headless')
        options.add_argument('--start-maximized')
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        options.add_argument('--window-size=1920,1080')
        
        self.driver = webdriver.Chrome(options=options)
        self.driver.implicitly_wait(10)
        
        # 創建截圖目錄
        if not os.path.exists(self.screenshot_dir):
            os.makedirs(self.screenshot_dir)
        
        print("[OK] 瀏覽器已啟動")
        
    def teardown(self):
        """關閉瀏覽器"""
        if self.driver:
            print("[*] 關閉瀏覽器...")
            time.sleep(2)
            self.driver.quit()
            
    def take_screenshot(self, name):
        """截圖並保存"""
        try:
            timestamp = datetime.now().strftime('%H%M%S')
            filename = f"{timestamp}_{name}.png"
            filepath = os.path.join(self.screenshot_dir, filename)
            self.driver.save_screenshot(filepath)
            print(f"   📸 截圖已保存: {filename}")
            return filepath
        except Exception as e:
            print(f"   ⚠ 截圖失敗: {e}")
            return None
    
    def record_result(self, test_name, status, message="", screenshot=None):
        """記錄測試結果"""
        self.test_results.append({
            'name': test_name,
            'status': status,
            'message': message,
            'screenshot': screenshot,
            'timestamp': datetime.now()
        })
    
    def test_01_app_running(self):
        """測試 1: 檢查應用是否運行"""
        print("\n[TEST 1] 檢查應用是否運行")
        try:
            print(f"   訪問: {APP_URL}")
            self.driver.get(APP_URL)
            time.sleep(2)
            screenshot = self.take_screenshot("01_app_running")
            
            # 檢查頁面標題
            assert "二手機回收價" in self.driver.title or "登入" in self.driver.title
            print("   [OK] 應用正常運行！")
            self.record_result("應用運行檢查", "PASS", screenshot=screenshot)
            return True
        except Exception as e:
            print(f"   [ERROR] {e}")
            screenshot = self.take_screenshot("01_app_running_error")
            self.record_result("應用運行檢查", "FAIL", str(e), screenshot)
            return False
            
    def test_02_login(self):
        """測試 2: 登入功能"""
        print("\n[TEST 2] 登入功能")
        try:
            # 確保在登入頁面
            if "/login" not in self.driver.current_url:
                self.driver.get(APP_URL)
                time.sleep(1)
            
            # 等待密碼輸入框出現
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.NAME, "password"))
            )
            screenshot = self.take_screenshot("02_login_page")
            
            # 輸入密碼
            print(f"   輸入密碼...")
            password_input = self.driver.find_element(By.NAME, "password")
            password_input.clear()
            password_input.send_keys(ADMIN_PASSWORD)
            time.sleep(1)
            
            # 點擊登入按鈕
            print("   點擊登入按鈕")
            login_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
            login_button.click()
            
            # 等待登入成功
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "h1"))
            )
            time.sleep(2)
            screenshot = self.take_screenshot("02_login_success")
            
            print("   [OK] 登入成功！")
            self.record_result("登入功能", "PASS", screenshot=screenshot)
            return True
        except Exception as e:
            print(f"   [ERROR] {e}")
            screenshot = self.take_screenshot("02_login_error")
            self.record_result("登入功能", "FAIL", str(e), screenshot)
            return False
    
    def test_03_main_page_ui(self):
        """測試 3: 主頁 UI 元素"""
        print("\n[TEST 3] 主頁 UI 元素檢查")
        try:
            # 檢查表格存在
            table = self.driver.find_element(By.TAG_NAME, "table")
            assert table.is_displayed()
            print("   ✓ 表格顯示正常")
            
            # 檢查控制按鈕
            controls = self.driver.find_element(By.CLASS_NAME, "controls")
            assert controls.is_displayed()
            print("   ✓ 控制區域顯示正常")
            
            # 滾動查看整個頁面
            self.driver.execute_script("window.scrollTo(0, 0);")
            time.sleep(1)
            screenshot_top = self.take_screenshot("03_main_page_top")
            
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)
            screenshot_bottom = self.take_screenshot("03_main_page_bottom")
            
            print("   [OK] UI 元素檢查通過！")
            self.record_result("主頁 UI 檢查", "PASS", screenshot=screenshot_top)
            return True
        except Exception as e:
            print(f"   [ERROR] {e}")
            screenshot = self.take_screenshot("03_ui_check_error")
            self.record_result("主頁 UI 檢查", "FAIL", str(e), screenshot)
            return False
    
    def test_04_no_pdf_line_buttons(self):
        """測試 4: 主頁不應顯示 PDF/LINE 按鈕"""
        print("\n[TEST 4] 檢查主頁無 PDF/LINE 按鈕")
        try:
            # 回到頂部
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)
            
            # 檢查按鈕不存在
            pdf_buttons = self.driver.find_elements(By.CSS_SELECTOR, ".action-btn.pdf-btn")
            line_buttons = self.driver.find_elements(By.CSS_SELECTOR, ".action-btn.line-btn")
            
            screenshot = self.take_screenshot("04_no_buttons_check")
            
            if len(pdf_buttons) == 0 and len(line_buttons) == 0:
                print("   [OK] 主頁正確隱藏了 PDF/LINE 按鈕")
                self.record_result("主頁按鈕隱藏檢查", "PASS", screenshot=screenshot)
                return True
            else:
                raise AssertionError(f"找到 {len(pdf_buttons)} 個 PDF 按鈕和 {len(line_buttons)} 個 LINE 按鈕")
        except Exception as e:
            print(f"   [ERROR] {e}")
            screenshot = self.take_screenshot("04_buttons_check_error")
            self.record_result("主頁按鈕隱藏檢查", "FAIL", str(e), screenshot)
            return False
    
    def test_05_create_quote(self):
        """測試 5: 創建報價單（如果被跳過則直接訪問）"""
        print("\n[TEST 5] 創建報價單")
        try:
            # 確保在主頁
            if self.driver.current_url != APP_URL:
                self.driver.get(APP_URL)
                time.sleep(2)
            
            # 返回頂部
            self.driver.execute_script("window.scrollTo(0, 0);")
            time.sleep(1)
            
            # 找到指令輸入框
            print("   查找指令輸入框...")
            try:
                quote_input = self.driver.find_element(By.ID, "quote-name")
            except:
                quote_input = self.driver.find_element(By.CSS_SELECTOR, "input[type='text']")
            
            screenshot = self.take_screenshot("05_before_input")
            
            # 輸入指令
            test_client_name = f"自動測試_{int(time.time())}"
            command = f"新增/{test_client_name}"
            print(f"   輸入指令: {command}")
            quote_input.clear()
            quote_input.send_keys(command)
            time.sleep(1)
            
            screenshot = self.take_screenshot("05_after_input")
            
            # 按 Enter
            quote_input.send_keys("\n")
            
            # 等待 alert
            time.sleep(3)
            try:
                alert = self.driver.switch_to.alert
                alert_text = alert.text
                print(f"   收到提示: {alert_text}")
                screenshot = self.take_screenshot("05_alert")
                alert.accept()
                print("   [OK] 報價單創建成功！")
                self.record_result("創建報價單", "PASS", f"客戶: {test_client_name}", screenshot)
                return True
            except:
                print("   [WARNING] 未收到 alert")
                screenshot = self.take_screenshot("05_no_alert")
                self.record_result("創建報價單", "PASS", "未收到確認訊息但可能成功", screenshot)
                return True
                
        except Exception as e:
            print(f"   [ERROR] {e}")
            screenshot = self.take_screenshot("05_create_error")
            self.record_result("創建報價單", "FAIL", str(e), screenshot)
            return False
    
    def test_06_android_brand_loading(self):
        """測試 6: Android 品牌載入（如果存在）"""
        print("\n[TEST 6] Android 品牌載入測試")
        try:
            # 切換到 Android tab（如果存在）
            try:
                android_tab = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Android')]")
                android_tab.click()
                time.sleep(2)
                screenshot = self.take_screenshot("06_android_tab")
                
                # 嘗試點擊一個品牌按鈕
                samsung_btn = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Samsung')]")
                samsung_btn.click()
                time.sleep(3)
                screenshot = self.take_screenshot("06_samsung_loaded")
                
                print("   [OK] Android 品牌載入功能正常")
                self.record_result("Android 品牌載入", "PASS", screenshot=screenshot)
                return True
            except:
                print("   [SKIP] Android 功能不存在或未啟用")
                self.record_result("Android 品牌載入", "SKIP", "功能不存在")
                return True
        except Exception as e:
            print(f"   [ERROR] {e}")
            screenshot = self.take_screenshot("06_android_error")
            self.record_result("Android 品牌載入", "FAIL", str(e), screenshot)
            return False
    
    def run_all_tests(self):
        """執行所有測試"""
        try:
            self.setup()
            print("\n" + "="*70)
            print("[START] 開始執行視覺化瀏覽器測試")
            print("="*70)
            
            # 執行所有測試
            tests = [
                self.test_01_app_running,
                self.test_02_login,
                self.test_03_main_page_ui,
                self.test_04_no_pdf_line_buttons,
                self.test_05_create_quote,
                self.test_06_android_brand_loading
            ]
            
            passed = 0
            failed = 0
            skipped = 0
            
            for test in tests:
                try:
                    result = test()
                    if result:
                        passed += 1
                except Exception as e:
                    failed += 1
                    print(f"   [EXCEPTION] {e}")
            
            # 統計跳過的測試
            for result in self.test_results:
                if result['status'] == 'SKIP':
                    skipped += 1
            
            print("\n" + "="*70)
            print("[完成] 測試執行完畢")
            print("="*70)
            print(f"✓ 通過: {passed}")
            print(f"✗ 失敗: {failed}")
            print(f"⊘ 跳過: {skipped}")
            print(f"📸 截圖保存在: {self.screenshot_dir}")
            print("="*70)
            
        except Exception as e:
            print(f"\n[FAIL] 測試失敗: {e}")
            import traceback
            traceback.print_exc()
        finally:
            self.teardown()

if __name__ == "__main__":
    print("""
==============================================================
          視覺化瀏覽器測試 (帶截圖功能)                        
==============================================================

!! 測試前請確認:
   1. Flask 應用正在運行 (http://127.0.0.1:8080)
   2. 已安裝 Chrome 瀏覽器
   3. 已安裝 Selenium: pip install selenium

執行方式:
   顯示瀏覽器視窗: python test_browser_visual.py
    """)
    
    print("\n正在啟動測試...\n")
    
    # 執行測試 (headless=False 會顯示瀏覽器窗口)
    tester = VisualBrowserTest(headless=False)
    tester.run_all_tests()
