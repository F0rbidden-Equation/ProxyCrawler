import requests
from bs4 import BeautifulSoup
import html
import argparse

# 🎨 Couleurs terminal
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
RESET = "\033[0m"

def get_proxies_from_page(page, nonce="67d2204174"):
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

    print(f"{YELLOW}[→] Scraping page {page}...{RESET}")
    response = requests.post(url, headers=headers, data=data)
    if response.status_code != 200:
        print(f"{RED}[!] Failed to fetch page {page}{RESET}")
        return []

    try:
        json_data = response.json()
        html_rows = html.unescape(json_data.get("data", {}).get("rows", ""))
    except Exception as e:
        print(f"{RED}[!] JSON error: {e}{RESET}")
        return []

    soup = BeautifulSoup(html_rows, "html.parser")
    proxies = []

    for row in soup.find_all("tr"):
        cols = row.find_all("td")
        if len(cols) >= 5:
            ip = cols[0].get_text(strip=True)
            port = cols[1].get_text(strip=True)
            protocol = cols[2].get_text(strip=True)
            try:
                country = cols[4].find("strong").get_text(strip=True)
            except:
                country = "Unknown"

            if "SOCKS5" in protocol.upper():
                proxies.append({
                    "ip": ip,
                    "port": port,
                    "protocol": protocol,
                    "country": country
                })

    return proxies

# ▶️ Programme principal
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="SOCKS5 Proxy Crawler from proxy5.net")
    parser.add_argument("--pages", type=int, default=5, help="Number of pages to scrape (default: 5)")
    args = parser.parse_args()

    # 🧼 Vider le fichier au lancement
    with open("proxy_list.txt", "w") as f:
        f.write("")

    print(f"{BLUE}🔎 Starting SOCKS5 proxy scan on {args.pages} pages...{RESET}\n")
