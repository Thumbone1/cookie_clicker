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


# -----------------------accept cookies, select english, find cookie--------------------------#

driver.implicitly_wait(5)  # wait for page to load

consent_button = driver.find_element(By.CLASS_NAME, "fc-cta-consent")
consent_button.click()

driver.implicitly_wait(5)  # Wait again

english_button = driver.find_element(By.ID, "langSelect-EN")
english_button.click()

driver.refresh()  # fixed the stale element errors

try:
    cookie = driver.find_element(By.ID, "bigCookie")
except Exception as e:
    print(f"{e} Tried and failed to get the big cookie")

# ---------------------------------------BOT functions----------------------------------------#


def click_element(num=1, element=cookie):
    # defaults to click the cookie once
    for _ in range(0, num):
        try:
            element.click()
        except Exception as e:
            print(f"Tried and failed to click the element {element}")
            pass


def find_upgrades():
    # returns a list of available upgrades, most advanced upgrade first.
    # If there are no available upgrades this runs painfully slow
    # but I can't find any advice other than what I have here.
    # Apparently this is the best selenium can do really. chat gpt
    # agrees so that's that lol.

    available_upgrades = []
    try:
        upgrades_parent = driver.find_element(By.ID, "upgrades")
        new_upgrades = upgrades_parent.find_elements(
            By.CSS_SELECTOR, ".crate.upgrade.enabled"
        )

        if new_upgrades:
            available_upgrades.extend(new_upgrades)
            print("\nupgrades available :", len(available_upgrades))
            return reversed(available_upgrades)
        else:
            return None
    except Exception as e:
        print(f"{e} no upgrades available, error")
        pass


def find_products():
    # returns a list of available products, most advanced upgrade first

    available_products = []
    try:
        products_parent = driver.find_element(By.ID, "products")
        new_products = products_parent.find_elements(
            By.CSS_SELECTOR, ".product.unlocked.enabled"
        )

        if new_products:
            available_products.extend(new_products)
            print("\nproducts:", len(available_products))
            return reversed(available_products)
        else:
            return None
    except Exception as e:
        print(f"{e} error when getting available products")
        pass


def early_game_strat(buy_p: bool):
    # This strat would works until you buy too many grandmas and they are like 70k per.
    # Then this will just be buying grandmas and clickers for an eternity.
    # With this strat that's around 7000cps.

    buy_product = buy_p  # this is set here to prevent emptying your cookie wallet every loop

    if find_upgrades() is not None:  # if there are upgrades then click them.
        for upgrade in find_upgrades():
            try:
                click_element(element=upgrade)
            except Exception as e:
                print(f"{e} error while trying to click upgrade")
                pass

    if (
        buy_product and find_products() is not None
    ):  # only buy products every other loop
        for product in find_products():
            num_cookies = int(
                driver.find_element(By.ID, "cookies")
                .text.replace(",", "")
                .split()[0]
            )  # check how many cookies I have

            while (
                int(
                    product.find_element(
                        By.CSS_SELECTOR, (".content .price")
                    ).text.replace(",", "")
                )
                < num_cookies
            ):
                click_element(element=product)
                num_cookies = int(
                    driver.find_element(By.ID, "cookies")
                    .text.replace(",", "")
                    .split()[0]
                )  # update num_cookies and keep buyin' if ya got some


def mid_game_strat():
    if find_upgrades() is not None:  # if there are upgrades then click them.
        for upgrade in find_upgrades():
            try:
                click_element(element=upgrade)
            except Exception as e:
                print(f"{e} error while trying to click upgrade")
                pass

    for product in find_products():
        product_price = int(
            product.find_element(
                By.CSS_SELECTOR, (".content .price")
            ).text.replace(",", "")
        )
        num_cookies = int(
            driver.find_element(By.ID, "cookies")
            .text.replace(",", "")
            .split()[0]
        )
        while (
            num_cookies / 2
        ) > product_price:  # should be saving some cookies here and using money on upgrades instead.
            click_element(element=product)


# -----------------------------------------main loop-------------------------------------------#


running = True
buy_products = True
cps_grapher = []
clickin_time = 15
while running:
    start_time = time.time()

    while (time.time() - start_time) < clickin_time:
        if keyboard.is_pressed(
            "q"
        ):  # have to press 'q' when clickin' is happenin'
            running = False
            break

        click_element()
    cps = int(
        driver.find_element(By.ID, "cookies").text.replace(",", "").split()[-1]
    )
    cps_grapher.append((time.time(), cps))

    if cps <= 5000:
        early_game_strat(buy_products)
        buy_products = not buy_products
    elif cps > 5000:
        mid_game_strat()
        clickin_time = 30

with open("cps_grapher.txt", "w") as file:
    file.write('\n'.join(f"{tup[0]} {tup[1]}" for tup in cps_grapher)) # used to create graph of cps over time

driver.quit()
