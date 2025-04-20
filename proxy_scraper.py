import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

def fetch_live_proxies_selenium(url="https://proxy5.net/free-proxy", clicks=5):
    print("[Infos] Launching headless browser...")
    options = Options()
    options.headless = True
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

    try:
        print("[Infos] Opening the proxy site...")
        driver.get(url)
        time.sleep(3)

        for i in range(clicks):
            try:
                print(f"[Click] Loading more proxies... ({i+1}/{clicks})")
                load_more_btn = driver.find_element(By.ID, "proxylister-load-more")
                driver.execute_script("arguments[0].click();", load_more_btn)
                time.sleep(2)  # Laisse le temps au contenu de charger
            except Exception as e:
                print("[Info] No more proxies or button not found.")
                break

        html = driver.page_source
    finally:
        driver.quit()

    soup = BeautifulSoup(html, "html.parser")
    tables = soup.find_all("table")
    proxy_pool = []

    for table in tables:
        rows = table.find_all("tr")
        for row in rows:
            cols = row.find_all("td")
            if len(cols) >= 5:
                ip = cols[0].get_text(strip=True)
                port = cols[1].get_text(strip=True)
                protocols = cols[2].get_text(strip=True)
                country_tag = cols[4].find("strong")
                country = country_tag.get_text(strip=True) if country_tag else "Unknown"

                if ip.count('.') == 3 and port.isdigit():
                    proxy_pool.append({
                        "ip": ip,
                        "port": port,
                        "protocol": protocols,
                        "country": country
                    })

    return proxy_pool


# 🔁 Exemple d'utilisation :
proxies = fetch_live_proxies_selenium()
print("\n[Infos] Proxy lists : OK")
print(f"[Infos] {len(proxies)} proxies loaded.")
print("[Infos] Rotate Circuits Proxy : Active!\n")

# 🧪 Affichage des proxies récupérés
print("[Debug] List of proxies:")
for index, proxy in enumerate(proxies, 1):
    print(f"[{index}] {proxy['ip']}:{proxy['port']} - {proxy['protocol']} - {proxy['country']}")

