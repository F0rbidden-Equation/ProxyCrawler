
import requests
import re
import time
from bs4 import BeautifulSoup

# 🎨 Terminal colors
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
RESET = "\033[0m"

# 📦 Chemin du fichier proxy sauvegardé
proxy_output = "proxy_list.txt"

# ➔ 1. Obtenir un nonce dynamique

def get_dynamic_nonce():
    print(f"{CYAN}[→] Fetching homepage to extract fresh nonce...{RESET}")
    try:
        response = requests.get("https://proxy5.net/free-proxy", headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
        response.raise_for_status()
        html = response.text

        match = re.search(r'"nonce":"([a-zA-Z0-9]+)"', html)
        if match:
            fresh_nonce = match.group(1)
            print(f"{GREEN}[✓] Nonce found dynamically: {fresh_nonce}{RESET}")
            return fresh_nonce
        else:
            print(f"{RED}[✗] Could not find nonce in page!{RESET}")
            return None

    except Exception as e:
        print(f"{RED}[!] Error fetching homepage: {e}{RESET}")
        return None

# ➔ 2. Télécharger et parser les proxies pour une page

def fetch_proxies_from_page(page, nonce):
    url = "https://proxy5.net/wp-admin/admin-ajax.php"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    data = {
        "action": "proxylister_load_more",
        "nonce": nonce,
        "page": str(page),
        "atts[downloads]": "true",
        "atts[sort_by]": "-uptime"
    }

    print(f"{CYAN}[→] Scraping page {page}...{RESET}")
    try:
        response = requests.post(url, headers=headers, data=data, timeout=10)
        response.raise_for_status()

        json_data = response.json()
        if 'data' in json_data and 'rows' in json_data['data']:
            return json_data['data']['rows']
        else:
            print(f"{RED}[!] No rows found on page {page}.{RESET}")
            return ""

    except Exception as e:
        print(f"{RED}[!] Error fetching page {page}: {e}{RESET}")
        return ""

# ➔ 3. Extraire IP, port et type à partir du HTML brut

def parse_proxies(html_raw):
    proxies = []
    soup = BeautifulSoup(html_raw, "html.parser")

    for row in soup.find_all("tr"):
        cols = row.find_all("td")
        if len(cols) >= 3:
            ip = cols[0].text.strip()
            port = cols[1].text.strip()
            protocol = cols[2].text.strip()

            # ➔ Ici on filtre uniquement SOCKS5 (tu peux enlever si tu veux tout)
            if "SOCKS5" in protocol.upper():
                proxies.append(f"{ip}:{port}")

    return proxies

# ➔ 4. Main process

def main():
    print(f"{CYAN}======================================")
    print(f"        Proxy Scraper by Amadeus")
    print(f"======================================{RESET}\n")

    pages_to_scrape = int(input("🔢 How many pages to scrape? (ex: 5): ").strip())

    nonce = get_dynamic_nonce()
    if not nonce:
        print(f"{RED}[!] Aborting - No valid nonce.{RESET}")
        return

    all_proxies = []

    for page in range(1, pages_to_scrape + 1):
        raw_html = fetch_proxies_from_page(page, nonce)
        if raw_html:
            page_proxies = parse_proxies(raw_html)
            all_proxies.extend(page_proxies)
        time.sleep(2)

    # ➔ Écraser le fichier existant
    with open(proxy_output, "w") as f:
        for proxy in all_proxies:
            f.write(proxy + "\n")

    print(f"\n{GREEN}✅ Scraping finished. Total proxies scraped: {len(all_proxies)}{RESET}")
    print(f"{CYAN}Proxies saved to {proxy_output}{RESET}")


if __name__ == "__main__":
    main()
