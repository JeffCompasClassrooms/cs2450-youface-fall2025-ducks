from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

# ---------- Setup ----------
options = Options()
options.add_argument("--headless")  # Run Chrome invisibly
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

selenium_url = os.getenv("SELENIUM_REMOTE_URL", "http://localhost:4444/wd/hub")
driver = webdriver.Remote(
    command_executor=selenium_url,
    options=options,
    desired_capabilities=DesiredCapabilities.CHROME
)

try:
    driver.get("http://127.0.0.1:5005")
    time.sleep(2)

    print("--= Beginning YouFace UI Tests =--")

    # ---------- Test 1: Page Title ----------
    title = driver.title
    if title:
        print(f"[PASSED] - Page title found: '{title}'")
    else:
        print("[FAILED] - No page title found.")

    # ---------- Test 2: Navbar Exists ----------
    try:
        navbar = driver.find_element(By.CSS_SELECTOR, "nav.navbar")
        print("[PASSED] - Navbar element found.")
    except:
        print("[FAILED] - Navbar not found.")

    # ---------- Test 3: Logo Image Exists ----------
    try:
        logo = driver.find_element(By.CSS_SELECTOR, "img[alt*='goose']")
        print("[PASSED] - Logo image found.")
    except:
        print("[FAILED] - Logo image missing.")

    # ---------- Test 4: Custom Stylesheet Loaded ----------
    try:
        styles = driver.find_elements(By.TAG_NAME, "link")
        found_custom_style = any(
            "style.css" in s.get_attribute("href") for s in styles if s.get_attribute("href")
        )
        if found_custom_style:
            print("[PASSED] - Custom stylesheet 'style.css' is linked.")
        else:
            print("[FAILED] - Custom stylesheet 'style.css' not found.")
    except Exception as e:
        print("[FAILED] - Error checking stylesheet link:", e)

    # ---------- Test 5: Collapsible Button ----------
    try:
        toggler = driver.find_element(By.CSS_SELECTOR, "button.navbar-toggler")
        print("[PASSED] - Navbar toggler button found.")
    except:
        print("[FAILED] - Navbar toggler button missing.")

    # ---------- Test 6: Jumbotron Heading ----------
    try:
        heading = driver.find_element(By.CSS_SELECTOR, ".jumbotron h1 a").text
        if heading:
            print(f"[PASSED] - Jumbotron heading text found: '{heading}'")
        else:
            print("[FAILED] - Jumbotron heading empty.")
    except:
        print("[FAILED] - Jumbotron heading missing.")

    # ---------- Test 7: Jumbotron Subtitle ----------
    try:
        subtitle = driver.find_element(By.CSS_SELECTOR, ".jumbotron p.lead").text
        if subtitle:
            print(f"[PASSED] - Subtitle text found: '{subtitle}'")
        else:
            print("[FAILED] - Subtitle text empty.")
    except:
        print("[FAILED] - Jumbotron subtitle missing.")

    # ---------- Test 8: Alert Container (Flashed Messages Area) ----------
    try:
        container = driver.find_element(By.CSS_SELECTOR, "div.container")
        alerts = container.find_elements(By.CSS_SELECTOR, "div.alert")
        print(f"[PASSED] - Found alert container; {len(alerts)} alerts rendered.")
    except:
        print("[FAILED] - Flash message container not found.")
    # --------- Test 9 ----------
    try:
        images = driver.find_elements(By.TAG_NAME, "img")
        all_have_alt = all(img.get_attribute("alt") for img in images)
        if all_have_alt:
            print("[PASSED] - All images have alt attributes.")
        else:
            print("[FAILED] - Some images are missing alt attributes.")
    except:
        print("[FAILED] - Error checking images for alt attributes.")

    # ---------- Test 10: Bootstrap JS Loaded ----------
    try:
        scripts = driver.find_elements(By.TAG_NAME, "script")
        found_bootstrap = any(
            "bootstrap" in s.get_attribute("src") for s in scripts if s.get_attribute("src")
        )
        if found_bootstrap:
            print("[PASSED] - Bootstrap JS script tag detected.")
        else:
            print("[FAILED] - Bootstrap JS not detected in page.")
    except:
        print("[FAILED] - Could not check for Bootstrap script tags.")

except Exception as e:
    print("Error during testing:", e)

finally:
    print("--= Ending YouFace UI Tests =--")
    driver.quit()
