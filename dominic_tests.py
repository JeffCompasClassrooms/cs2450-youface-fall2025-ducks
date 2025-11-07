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
    driver.get("http://127.0.0.1:5005/signup")
    time.sleep(2)

    print("--= Beginning Tests =--")
    submit = driver.find_element(By.CSS_SELECTOR, "input[type='submit'][value='CREATE ACCOUNT']")
    form = driver.find_element(By.CSS_SELECTOR, "#signup_page")
    age = driver.find_element(By.CSS_SELECTOR, "#age")
    minAge = driver.find_element(By.CSS_SELECTOR, "#minAge")
    maxAge = driver.find_element(By.CSS_SELECTOR, "#maxAge")
    name = driver.find_element(By.CSS_SELECTOR, "#nameText").text
    quest1 = driver.find_element(By.CSS_SELECTOR, "#question1")
    answer1 = driver.find_element(By.CSS_SELECTOR, "#prompt1")
    quest3 = driver.find_element(By.CSS_SELECTOR, "#question3")
    answer3 = driver.find_element(By.CSS_SELECTOR, "#prompt3")

    if age:
        print("[PASSED] - There is an age field")
    else:
        print("[FAILED] - There is no age field")

    if quest1:
        print("[PASSED] - Question 1 exist")
    else:
        print("[FAILED] - Question 1 does not exist")

    if answer1:
        print("[PASSED] - There is a field to submit answers")
    else:
        print("[FAILED] - No field found")

    if name == "FIRST NAME":
        print("[PASSED] - Label is correct.")
    else:
        print("[FAILED] - Label is not correct")

    if minAge:
        print("[PASSED] - minimum age field exists.")
    else:
        print("[FAILED] - minimum age not found.")

    if maxAge:
        print("[PASSED] - maximum age field exists.")
    else:
        print("[FAILED] - max age not founds not found.")


    if submit:
        print("[PASSED] - Submit button exists.")
    else:
        print("[FAILED] - Submit not found.")

    if form:
        print("[PASSED] - Form Exists.")
    else:
        print("[FAILED] - Form not found.")

    if quest3:
        print("[PASSED] - Question 3 exist")
    else:
        print("[FAILED] - Question 3 does not exist")

    if answer3:
        print("[PASSED] - There is a field to submit answers")
    else:
        print("[FAILED] - No field found")

except Exception as e:
    print("Error:", e)

finally:
    print("--= Ending Tests =--")
    driver.quit()
