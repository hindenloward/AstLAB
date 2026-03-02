from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
import time

# --- Setup Chrome ---
chrome_options = Options()
chrome_options.add_argument("--headless")  # remove if you want to see browser
chrome_options.add_argument("--window-size=1920,1080")

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=chrome_options
)

# --- Load page ---
url = "https://www.coloradonationalgolfclub.com/tee-times"
driver.get(url)

iframes = driver.find_elements(By.TAG_NAME, "iframe")
for i, iframe in enumerate(iframes):
#    print(i, iframe.get_attribute("src"))

    driver.switch_to.frame(iframes[0])
#print("Switched into iframe")
WebDriverWait(driver, 20).until(
    EC.presence_of_element_located(
        (By.CSS_SELECTOR, '[data-testid="teetimes-tile-time"]')
    )
)
# wait for JS to load tee times
time.sleep(5)

driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
time.sleep(2)

#with open("debug.html", "w", encoding="utf-8") as f:
#    f.write(driver.page_source)

#print("Saved debug.html")

# --- Parse rendered HTML ---
soup = BeautifulSoup(driver.page_source, "html.parser")
times = soup.find_all("p", {"data-testid": "teetimes-tile-time"})
players = soup.find_all("p", {"data-testid": "teetimes-tile-available-players"})
holes = soup.find_all("p", {"data-testid": "teetimes-tile-hole-verbiage"})
price = soup.find_all("p", string=re.compile(r"\$\d+\.\d{2}"))
#print(f"Times found: {len(times)}")
#print(f"Players found: {len(players)}")
#print(f"Holes found: {len(holes)}")
#print(f"Price found: {len(price)}")
print("COLORADO NATIONAL, ERIE:")
for t, p, h, pr in zip(times, players, holes, price):
    print(f"{t.text.strip()} — Players available: {p.text.strip()} — Holes: {h.text.strip()} - Price: {pr.text.strip()}")
# --- Scrape date ---
date_button = soup.find("button", {"data-testid": "teetimes-header-date-link"})
date_text = date_button.text.strip() if date_button else "Date not found"

print("Date:", date_text)

# tiles = soup.find_all("div", {"data-testid": "teetimes-tile"})

# for tile in tiles:
#     time_el = tile.find("p", {"data-testid": "teetimes-tile-time"})
#     players_el = tile.find("p", {"data-testid": "teetimes-tile-available-players"})
#     holes_el = tile.find("p", {"data-testid": "teetimes-tile-hole-verbiage"})
#     price = "Price N/A"

#     if time_el and players_el and holes_el:
#         time = time_el.text.strip()
#         players = players_el.text.strip()
#         holes = holes_el.text.strip() if holes_el else "Holes not available"
#         print(f"{time} — Players available: {players} — Holes: {holes} — Price: {price}")

driver.quit()