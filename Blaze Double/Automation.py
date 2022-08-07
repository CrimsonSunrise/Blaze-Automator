import selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import requests
import json

BASE_URL = 'https://blaze.com/pt/games/double'

class Bot:
    
    driver = None
    LOGIN_SUCCESS = None
    
    ACCOUNT_BALANCE = None
    
    # Start | Start selenium library, open the browser and load the webpage
    def Start(self, headless):
        
        print("Starting Bot")
        
        global driver
        
        chrome_options = Options()
        chrome_options.add_argument("--window-size=1300,1000")
        chrome_options.add_experimental_option("detach", True)
        
        if headless == True:
            chrome_options.add_argument("--headless")
        
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
            
            time.sleep(1)
            LOGIN_CONFIRMATION = driver.find_element(By.CLASS_NAME, 'description')
            if LOGIN_CONFIRMATION:
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
    def Bet(self, bets, return_results):
        
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
            current_status = requests.get('https://blaze.com/api/roulette_games/current').json()['status']
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
            INPUT_AMOUNT.send_keys(str(bet[1]))
            
            time.sleep(0.2)
            if bet['color'].lower() == "red":
                RED_BUTTON.click()
            elif bet['color'].lower() == "black":
                BLACK_BUTTON.click()
            elif bet['color'].lower() == "white":
                WHITE_BUTTON.click()
            
            time.sleep(0.2)
            BET_BUTTON.click()
            
            print("color:", bet['color'])
            print("amount:", bet['amount'])
        
        # Check for the results
        if return_results == True:
            
            current_result = None
            current_status = None
            while current_status != "complete":
                current_result = requests.get('https://blaze.com/api/roulette_games/current').json()
                current_status = current_result['status']
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