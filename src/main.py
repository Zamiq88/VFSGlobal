import time
from DrissionPage import ChromiumPage , ChromiumOptions
from bypass import CloudflareBypasser




class VfsGlobalBot():
    def __init__(self):
        # Initialize DrissionPage with necessary options
        chromium_options = ChromiumOptions()
        chromium_options.set_argument(('--headless'))
        chromium_options.set_argument("--remote-debugging-port=9222")
        chromium_options.set_argument( "-use-mock-keychain")
        chromium_options.set_argument( "--disable-blink-features=AutomationControlled")

        arguments = [#'-headless',
                "-no-first-run",
                "-force-color-profile=srgb",
                "-metrics-recording-only",
                "-password-store=basic",
                "-use-mock-keychain",
                "-export-tagged-pdf",
                "-no-default-browser-check",
                "-disable-background-mode",
                "-enable-features=NetworkService,NetworkServiceInProcess,LoadCryptoTokenExtension,PermuteTLSExtensions",
                "-disable-features=FlashDeprecationWarning,EnablePasswordsAccountStorage",
                "-deny-permission-prompts",
                "-disable-gpu",
                "-accept-lang=en-US",
                #"-incognito"  # Uncomment if you want incognito mode
                "--remote-debugging-port=9222"  # Optional
            ]
        # for arg in arguments:
        #     chromium_options.set_argument(arg)
        
        #chromium_options._is_headless = False  # Keep browser visible
        
        
        # Create a single ChromiumPage instance for everything
        self.page = ChromiumPage(chromium_options)
        
        # Initialize the Cloudflare bypasser
        self.cf_bypasser = CloudflareBypasser(self.page, max_retries=5)
        
    def target_url(self, url):
        # Navigate to the URL
        self.page.get(url)
        self.page.wait.doc_loaded(timeout=10)

        time.sleep(3)
        self.cf_bypasser.bypass()



        
        
        # Attempt to bypass Cloudflare if needed
           # self.cf_bypasser.bypass()
        
        # Optional: Wait for the page to fully load
        time.sleep(5)
    def enter_login_details(self):
        try:
            cookie_button = self.page.ele('#onetrust-accept-btn-handler', timeout=5)
            if cookie_button:
                cookie_button.click()
                print("✅ Clicked cookie accept button")
                time.sleep(2)  # Allow popup to disappear
        except:
            print("ℹ️ No cookie popup found.")
                    # ✅ Enter email
        email_field = self.page.wait.ele_displayed('#email', timeout=10)
        if email_field:
            email_field.clear()
            email_field.input("nuriyevzamiq@gmail.com")
            print("✅ Entered email successfully")
        else:
            print("❌ Email field not found")
           
        time.sleep(2)  
            # ✅ Enter password
        password_field = self.page.wait.ele_displayed('#password', timeout=5)
        if password_field: 
            password_field.clear()
            password_field.input("Kalytfabo88?")
            print("✅ Entered password successfully")
        else:
            print("❌ Password field not found") 


    def login(self):
        self.page.wait.doc_loaded(timeout=10)
        time.sleep(3)

            # ✅ Ensure page is fully loaded by waiting for the body element
        
            # ✅ Handle cookie consent popup if present
        try:
            cookie_button = self.page.ele('#onetrust-accept-btn-handler', timeout=5)
            if cookie_button:
                cookie_button.click()
                print("✅ Clicked cookie accept button")
                time.sleep(2)  # Allow popup to disappear
        except:
            print("ℹ️ No cookie popup found.")
            

            
            
        time.sleep(5)  # Give UI time to process inputs
        self.page.wait.doc_loaded()
        
        sign_in_button = self.page._find_elements("Sign In", timeout=10)
          # Set a limit to prevent infinite loops
        attempt = 0

        while not self.is_logged_in():
            if attempt >= 8:
                print("❌ Max retries reached. Login may have failed.")
                break
            if attempt>1 and not self.is_logged_in() and not self.cf_bypasser.is_bypassed():
                print('Trying again to bypass')
                self.page.refresh()
                time.sleep(8)
                self.page.get_screenshot('refresh2.png')
                self.cf_bypasser.bypass()
                self.enter_login_details()
                time.sleep(3)
                


            try:
                print(f"🔄 Attempt {attempt + 1}: Clicking 'Sign In' button...")
                
               
                

                if sign_in_button:
                    sign_in_button.click()
                    time.sleep(6)  # Allow time for login to process
                else:
                    print("⚠️ 'Sign In' button not found anymore. Assuming login attempt was successful.")

            except Exception as e:
                print(f"❌ Error clicking 'Sign In' button: {e}")

            attempt += 1
    def get_available_slots(self):
        # Wait for page to fully load
        print("Waiting for page to fully load...")
        time.sleep(5)
        self.page.wait.doc_loaded(timeout=15)
        
        print(f"Current URL: {self.page.url}")
        
        # Try using JavaScript to find and click the button
        print("Attempting to use JavaScript to find and click the button...")
        
        # Method 1: Try to find by button text
        js_result = self.page.run_js('''
            const buttons = Array.from(document.querySelectorAll('button'));
            for (let btn of buttons) {
                if (btn.textContent.includes('Start New Booking')) {
                    btn.click();
                    return true;
                }
            }
            return false;
        ''')
        
        if js_result:
            print("✅ Found and clicked 'Start New Booking' button using JavaScript text search")
            time.sleep(3)
        print("Attempting to select Tourism visa category...")
        self.page.wait.doc_loaded(timeout=10)
# ✅ Step 1: Open the 3rd dropdown
        js_double_click_third_dropdown = '''
        const dropdowns = document.querySelectorAll('mat-select');
        if (dropdowns.length >= 3) {
            dropdowns[2].click();  // Click the 3rd dropdown (index 2)
            setTimeout(() => dropdowns[2].click(), 1000);  // Click again after 1 second
            return true;
        }
        return false;
        '''
        js_result = self.page.run_js(js_double_click_third_dropdown)

        if js_result:
            print("✅ Clicked the 3rd dropdown twice with a 1-second interval.")
        else:
            print("❌ Could not find the 3rd dropdown.")
        time.sleep(3)  # 🔴 Increased wait time for options to load

            # ✅ Step 2: Wait for options to load


            # ✅ Step 3: Select "Tourism"
        js_select_tourism = '''
            const options = Array.from(document.querySelectorAll('mat-option'));
            for (let option of options) {
                if (option.textContent.includes('Tourism')) {
                    option.click();
                    return true;
                }
            }
            return false;
            '''
        js_result = self.page.run_js(js_select_tourism)

        if js_result:
            print("✅ Selected 'Tourism' successfully!")
        else:
            print("❌ 'Tourism' option still not found. It may be in another container.")
        time.sleep(2)
        js_check_no_slots = '''
        const noSlotsMessage = document.querySelector('.alert-info-blue');
        return noSlotsMessage ? noSlotsMessage.textContent.includes('no appointment slots') : false;
        '''
        no_slots = self.page.run_js(js_check_no_slots)

        if no_slots:
            print("❌ No appointment slots available.")
        



    
    def is_logged_in(self):
        if 'dashboard' in self.page.url.lower():
            print("URL changed after login, likely successful")
            return True

    
    def close(self):
        # Close the browser
        if hasattr(self, 'page') and self.page:
            self.page.quit()


# Example usage
if __name__ == "__main__":
    bot = VfsGlobalBot()
    bot.target_url('https://visa.vfsglobal.com/aze/en/ita/login')
    bot.enter_login_details()
    bot.login()
    bot.get_available_slots()
    time.sleep(60)
    bot.close()  # Make sure browser is closed properly