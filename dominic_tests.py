from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

# Don't specify chromedriver path!
driver = webdriver.Chrome(options=options)

try:
    driver.get("http://localhost:3000/signup")
    time.sleep(2)

    print("--= Beginning Tests =--")
    submit = driver.find_element(By.CSS_SELECTOR, "input[type='submit'][value='CREATE ACCOUNT']")
    form = driver.find_element(By.CSS_SELECTOR, "#signup_page")

    if submit  == "A billion dollars and it's yours!":
        print("[PASSED] - Submit button exists.")
    else:
        print("[FAILED] - Submit not found.")

    if form:
        print("[PASSED] - Form Exists.")
    else:
        print("[FAILED] - Form not found.")

except Exception as e:
    print("Error:", e)

finally:
    print("--= Ending Tests =--")
    driver.quit()
