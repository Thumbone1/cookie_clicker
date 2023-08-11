import time
import keyboard
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


chrome_driver_path = ChromeDriverManager().install()
my_service = ChromeService(executable_path=chrome_driver_path)

driver = webdriver.Chrome(service=my_service)
driver.get("https://orteil.dashnet.org/cookieclicker/")


#-------------------------accept cookies, select english, find cookie--------------------------#

driver.implicitly_wait(5)  # wait for page to load

consent_button = driver.find_element(By.CLASS_NAME, "fc-cta-consent")
consent_button.click()

driver.implicitly_wait(5)  # Wait again

english_button = driver.find_element(By.ID, "langSelect-EN")
english_button.click()


#-----------------get info-------------------#
driver.refresh() #maybe this will fix the stale element errors


try:
    cookie = driver.find_element(By.ID, "bigCookie")
except Exception as e:
    print(f"{e} Tried and failed to get the big cookie")
    
try:
    num_cookies = int(driver.find_element(By.ID, "cookies").text.split()[0])
    num_cps = float(driver.find_element(By.ID, "cookies").text.split()[-1])
except Exception as e:
    print(f"{e} Tried and failed to get number of cookies")





#----------------------------------helper functions------------------------------#


def click_element(num=1, element=cookie):
    #defaults to click the cookie once
    for _ in range(0, num):
        try:
            element.click()
        except Exception as e:
            print("Tried and failed to click the cookie")

#TODO: only add things that exist to the arr, then click them.
def find_bling():
    try:
        upgrade_ids = [f"upgrade{i}" for i in range(18)]
        available_upgrades = [driver.find_element(By.ID, upgrade_id) for upgrade_id in upgrade_ids if driver.find_element(By.ID, upgrade_id).get_property(By.CLASS_NAME) == "enabled"]
        print(available_upgrades)
    except:
        pass

    try:
        product_ids = [f"product{i}" for i in range(18)]
        available_products = [driver.find_element(By.ID, product_id) for product_id in product_ids if driver.find_element(By.ID, product_id).get_property(By.CLASS_NAME) == "enabled"]
        print(available_products)
    except:
        pass



#-----------------------main loop------------------------------#


running = True
while running:
    start_time = time.time()
    while (time.time() - start_time) < 20:
        if keyboard.is_pressed("q"):
            running = False
            break
        try:
            cookie.click()
        except Exception as e:
            print("Tried and failed to click the cookie")
        
    find_bling()

    

    

driver.quit()
