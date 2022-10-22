import selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import requests
import json

class Bot:
    
    driver = None
    LOGIN_SUCCESS = None
    
    ACCOUNT_BALANCE = None
    BASE_URL = ""
    
    # Start | Start selenium library, open the browser and load the webpage
    def Start(self):
        
        print("Starting Bot")
        
        global BASE_URL
        BASE_URL = 'https://blaze.com/pt/games/double'
            
        global driver
        
        chrome_options = Options()
        chrome_options.add_argument("--window-size=1300,1000")
        chrome_options.add_experimental_option("detach", True)
        
        chrome_options.add_argument("--log-level=3")
        user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36"
        chrome_options.add_argument(f"user-agent={user_agent}")
        driver = webdriver.Chrome(options=chrome_options)
        driver.set_window_position(500, 0, windowHandle="current")
        driver.get(BASE_URL)
        
        print("Bot started")
    
    # Stop | Close all selenium instances and processes
    def Stop(self):
        
        print("Bot is stopping")
        driver.quit()
        print("Bot stopped")
    
    # Login
    def Login(self, email, password):
        
        error = None
        global LOGIN_SUCCESS
        
        try:
            wait = WebDriverWait(driver, 10)
            LOGIN_BUTTON = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="header"]/div[2]/div/div[2]/div/div/div[1]/a')))
            LOGIN_BUTTON.click()
            
            time.sleep(1)
            EMAIL_INPUT = driver.find_elements(By.CLASS_NAME, 'input-wrapper')[0].find_element(By.TAG_NAME, 'input')
            EMAIL_INPUT.send_keys(email)
            
            PASSWORD_INPUT = driver.find_elements(By.CLASS_NAME, 'input-wrapper')[1].find_element(By.TAG_NAME, 'input')
            PASSWORD_INPUT.send_keys(password)
            
            SUBMIT_BUTTON = driver.find_element(By.CLASS_NAME, 'submit')
            SUBMIT_BUTTON.click()
            
            # You have to solve the captcha for it to continue
            while len(driver.find_elements_by_class_name("description")) == 0:
                time.sleep(1)
            
            LOGIN_SUCCESS = True
            
        except Exception as e:
            error = [False, e]
        finally:
            if error:
                print("Error", error)
                LOGIN_SUCCESS = False
                return error
            else:
                print("Login successful")
                Bot.Get_Balance(self)
                return [LOGIN_SUCCESS, None]
    
    # Balance
    def Get_Balance(self):
        
        error = None
        result = None
        
        global ACCOUNT_BALANCE
        
        try:
            balance_description = driver.find_element(By.CLASS_NAME, 'description').get_attribute("textContent")
            
            currency = None
            symbol = None
            
            if "R$" in balance_description:
                currency = "BRL"
                symbol = "R$"
            elif "$" in balance_description:
                currency = "USD"
                symbol = "$"
            elif "€" in balance_description:
                currency = "EUR"
                symbol = "€"
            
            balance = balance_description.split("(")[1].replace(")", "").replace(symbol, "")
            real = float(balance.split("+")[0].strip())
            bonus = float(balance.split("+")[1].strip().split(" ")[0])
            
            result = [real, bonus, currency]
        except:
            error = False
            print("Something went wrong")
            return error
        finally:
            if error == None:
                ACCOUNT_BALANCE = result
                return result
    
    # Bet
    def Bet(self, game, bets, return_results):
        global driver
        global BASE_URL
        
        if game == "crash":
            BASE_URL = 'https://blaze.com/pt/games/crash'
            driver.get(BASE_URL)
            return self.BetCrash([bets[0]], return_results)
        
        if game == "double":
            BASE_URL = 'https://blaze.com/pt/games/double'
            driver.get(BASE_URL)
            return self.BetDouble(bets, return_results)
    
    def BetDouble(self, bets, return_results):
        
        total_bet = 0
        
        # Check if bets are well formated and if the balance is enough
        for bet in bets:
            if len(bet) < 2 or isinstance(bet['color'], str) == False:
                print("Bad formatting", "sizes")
                return False
            
            if bet['color'].lower() == "white" or bet['color'].lower() == "black" or bet['color'].lower() == "red":
                pass
            else:
                print("Bad formatting", "wrong color name")
                return False
            
            if bet['amount'] * 1 > 0:
                total_bet += bet['amount']
            else:
                print("Bad formatting", "wrong amount")
                return False
            
        if total_bet > ACCOUNT_BALANCE[0]:
            print("You don't have enough balance")
            return False
        
        # Wait for the next bet window
        current_status = None
        while current_status != "waiting":
            current_status = requests.get('https://blaze.com/api/roulette_games/current')
            if current_status.status_code == 200:
                    current_status = current_status.json()['status']
            time.sleep(1)
        
        # Get the input and buttons reference
        
        INPUT_AMOUNT = driver.find_element(By.XPATH, '//*[@id="roulette-controller"]/div[1]/div[2]/div[1]/div/div[1]/input')
        RED_BUTTON = driver.find_element(By.XPATH, '//*[@id="roulette-controller"]/div[1]/div[2]/div[2]/div/div[1]')
        BLACK_BUTTON = driver.find_element(By.XPATH, '//*[@id="roulette-controller"]/div[1]/div[2]/div[2]/div/div[3]')
        WHITE_BUTTON = driver.find_element(By.XPATH, '//*[@id="roulette-controller"]/div[1]/div[2]/div[2]/div/div[2]')
        BET_BUTTON = driver.find_element(By.XPATH, '//*[@id="roulette-controller"]/div[1]/div[3]/button')
        
        # Perform bet
        for bet in bets:
            
            INPUT_AMOUNT.clear()
            INPUT_AMOUNT.send_keys(str(bet['amount']))
            
            time.sleep(0.2)
            if bet['color'].lower() == "red":
                RED_BUTTON.click()
            elif bet['color'].lower() == "black":
                BLACK_BUTTON.click()
            elif bet['color'].lower() == "white":
                WHITE_BUTTON.click()
            
            time.sleep(0.2)
            BET_BUTTON.click()
            
            print(bet)
        
        # Check for the results
        if return_results == True:
            
            current_result = None
            current_status = None
            while current_status != "complete":
                result = requests.get('https://blaze.com/api/roulette_games/current')
                if result.status_code == 200:
                    current_status = result.json()['status']
                    current_result = result.json()
                time.sleep(1)
            
            result_color = None
            multiplier = None
            
            if current_result['color'] == 0:
                result_color = "white"
                multiplier = 14
            elif current_result['color'] == 1:
                result_color = "red"
                multiplier = 1
            elif current_result['color'] == 2:
                result_color = "black"
                multiplier = 1
            
            bet_results = []
            total_result = 0
            
            for bet in bets:
                result = None
                if bet['color'] == result_color:
                    result = bet['amount'] * multiplier
                else:
                    result = 0 - bet['amount']
                
                total_result += result
                bet_results.append({ "color": bet['color'], "amount": result})
                
            print([total_result, bet_results])
            return [total_result, bet_results]
    
    def BetCrash(self, bets, return_results):
        
        total_bet = 0
        
        # Check if bets length is greater than 1
        if len(bets) > 1:
            print("Crash bets only can receive 1 object")
            return False
        
        # Check if bets are well formated and if the balance is enough
        for bet in bets:
            if len(bet) < 2:
                print("Bad formatting", "sizes")
                return False
            
            if bet['amount'] * 1 > 0:
                total_bet += bet['amount']
            else:
                print("Bad formatting", "wrong amount")
                return False
            
        if total_bet > ACCOUNT_BALANCE[0]:
            print("You don't have enough balance")
            return False
        
        # Wait for the next bet window
        current_status = None
        while current_status != "waiting":
            current_status = requests.get('https://blaze.com/api/crash_games/current')
            if current_status.status_code == 200:
                    current_status = current_status.json()['status']
            time.sleep(1)
        
        # Get the input and buttons reference
        INPUT_AMOUNT = driver.find_element(By.XPATH, '//*[@id="crash-controller"]/div[1]/div[2]/div[1]/div[1]/div/div[1]/input')
        INPUT_AUTO_REMOVE = driver.find_element(By.XPATH, '//*[@id="crash-controller"]/div[1]/div[2]/div[1]/div[2]/div[1]/input')
        BET_BUTTON = driver.find_element(By.XPATH, '//*[@id="crash-controller"]/div[1]/div[2]/div[2]/button')
        
        # Perform bet
        for bet in bets:
            
            INPUT_AMOUNT.clear()
            INPUT_AMOUNT.send_keys(str(bet['amount']))
            
            time.sleep(0.2)
            if bet['autoCashout'] > 1.00:
                INPUT_AUTO_REMOVE.clear()
                INPUT_AUTO_REMOVE.send_keys(str(bet['autoCashout']))
            else:
                INPUT_AUTO_REMOVE.clear()
                INPUT_AUTO_REMOVE.send_keys('1.01')
            
            time.sleep(0.2)
            BET_BUTTON.click()
            
            print(bet)
        
        # Check for the results
        if return_results == True:
            
            current_result = None
            current_status = None
            while current_status != "complete":
                result = requests.get('https://blaze.com/api/crash_games/current')
                if result.status_code == 200:
                    current_status = result.json()['status']
                    current_result = result.json()
                time.sleep(1)
            
            result_crash = float(current_result['crash_point'])
            print("res", result_crash)
            
            bet_results = []
            total_result = 0
            
            for bet in bets:
                result = None
                if bet['autoCashout'] <= result_crash:
                    result = bet['autoCashout'] * bet['amount']
                else:
                    result = 0 - bet['amount']
                
                total_result += result
                bet_results.append({ "autoCashout": bet['autoCashout'], "amount": result})
                
            print([total_result, bet_results])
            return [total_result, bet_results]