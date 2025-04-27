import requests
import random
import time
import os

# 🎨 Terminal colors
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
RESET = "\033[0m"

proxy_list_path = "proxy_list.txt"
working_proxy_path = "working_proxies.txt"

# 📦 Charger les proxys
def load_proxies(path=proxy_list_path):
    if not os.path.exists(path):
        print(f"{RED}[!] Proxy list not found: {path}{RESET}")
        return []
    with open(path, "r") as f:
        proxies = [line.strip() for line in f if line.strip()]
    print(f"{GREEN}📦 Loaded {len(proxies)} proxies from {path}{RESET}")
    return proxies

def get_random_proxy(proxy_list):
    proxy = random.choice(proxy_list)
    return {
        "http": f"socks5h://{proxy}",
        "https": f"socks5h://{proxy}"
    }

# [1] Enumération par Google Dork (placeholder)
def check_enum_pages(proxy_list):
    print(f"{CYAN}\n[1] Google Dork Enum (coming soon...){RESET}")
    def check_enum_pages(proxy_list):
    print(f"\n{CYAN}[1] Google Dork Enum – site + dorks + proxy rotation{RESET}")

    domain = input("🌐 Enter target domain (ex: example.com): ").strip()

    # Charger les dorks
    try:
        with open("dorks.txt", "r") as f:
            dorks = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"{RED}[!] dorks.txt not found.{RESET}")
        return

    if not proxy_list:
        print(f"{RED}[!] No proxies loaded. Aborting.{RESET}")
        return

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    request_count = 0
    proxy = get_random_proxy(proxy_list)

    for dork in dorks:
        if request_count % 5 == 0:
            proxy = get_random_proxy(proxy_list)
            print(f"{YELLOW}🔁 [Rotation] New Proxy: {proxy['http']}{RESET}")

        query = f"site:{domain} {dork}"
        url = "https://www.google.com/search?q=" + requests.utils.quote(query)

        print(f"\n🔍 Query: {query}")
        print(f"{CYAN}→ {url}{RESET}")

        try:
            resp = requests.get(url, proxies=proxy, headers=headers, timeout=10)
            soup = BeautifulSoup(resp.text, "html.parser")

            # Cherche les liens dans les résultats
            results = soup.find_all("a")
            found = False
