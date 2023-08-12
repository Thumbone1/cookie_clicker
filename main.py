# This program will play cookie clicker like it's the only thing it was made for
# The program will work until you surpass 999,999 cookies per second or
# 999 quadrillion cookies.

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


def extract_number(value_lst) -> int:
    # This will handle the string number values in cookie clicker.
    # need to pass a list with 2 elements as cookie clicker uses
    # 'x,xxx cookies' or 'x.xx million cookies' for counting and
    # includes cps in the HTML element. That's why num_cookies takes
    # the first two values of the list and cps takes the last value.
    # it's also why I turn text into a list then switch back to a string...
    value_str = " ".join(value_lst)

    suffixes = {
        "million": 10**6,
        "billion": 10**9,
        "trillion": 10**12,
        "quadrillion": 10**15,
    }  # if you pass quadrillion cookies then that's great for you. Go outside.

    for suffix, multiplier in suffixes.items():
        if suffix in value_str:
            value_float = float("".join(filter(str.isdigit, value_str)))
            value_int = int(value_float * multiplier)
            return value_int

    value_int = int(value_lst[0].replace(",", ""))
    return value_int


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
            num_cookies = extract_number(
                driver.find_element(By.ID, "cookies").text.split()[:2]
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
                num_cookies = extract_number(
                    driver.find_element(By.ID, "cookies").text.split()[:2]
                )  # update num_cookies and keep buyin' if ya got some


def mid_game_strat(buy_p: bool):
    # After an hour of running early_game_strat I decided to add this for cps > 5000.
    # prevents grandmapacolypse

    buy_product = buy_p

    if find_upgrades() is not None:  # if there are upgrades then click them.
        for upgrade in find_upgrades():
            try:
                click_element(element=upgrade)
            except Exception as e:
                print(f"{e} error while trying to click upgrade")
                pass
    if buy_product and find_products() is not None:
        for product in find_products():
            product_price = int(
                product.find_element(
                    By.CSS_SELECTOR, (".content .price")
                ).text.replace(",", "")
            )
            num_cookies = extract_number(
                driver.find_element(By.ID, "cookies").text.split()[:2]
            )

            while (
                num_cookies / 2.0
            ) > product_price:  # should be saving some cookies here and using money on upgrades instead.
                click_element(element=product)

                num_cookies = extract_number(
                    driver.find_element(By.ID, "cookies").text.split()[:2]
                )  # update num_cookies and keep buyin' if ya got some
                product_price = int(
                    product.find_element(
                        By.CSS_SELECTOR, (".content .price")
                    ).text.replace(
                        ",", ""
                    )  # update product price
                )


# -----------------------------------------main loop-------------------------------------------#


running = True
buy_products = True
cps_grapher = []
clickin_time = 15
grapher_start_time = time.time()
while running:
    start_time = time.time()

    while (time.time() - start_time) < clickin_time:
        if keyboard.is_pressed(
            "q"
        ):  # have to press 'q' when clickin' is happenin' to quit
            running = False
            break

        click_element()
    # This will only work up to 999,999 cps.
    # This and anything over 999 quadrillion will crash the program
    cps = float(
        driver.find_element(By.ID, "cookies").text.replace(",", "").split()[-1]
    )

    if cps <= 3000:
        early_game_strat(buy_products)
    elif cps > 3000:
        mid_game_strat(buy_products)
        clickin_time = 30

    buy_products = not buy_products

    grapher_total_time = int(time.time() - grapher_start_time)
    cps_grapher.append((grapher_total_time, cps))

with open("cps_grapher.txt", "w") as file:
    file.write(
        "\n".join(f"{tup[0]} {tup[1]}" for tup in cps_grapher)
    )  # used to create graph of cps over time

driver.quit()
