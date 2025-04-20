import requests
from bs4 import BeautifulSoup

def fetch_live_proxies(url="https://proxy5.net/free-proxy"):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    try:
        print("[Infos] Loading proxy address, please wait...")
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"[Error] Could not fetch proxies: {e}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    tables = soup.find_all("table")
    proxy_pool = []

    for table in tables:
        rows = table.find_all("tr")
        for row in rows:
            cols = row.find_all("td")
            if len(cols) >= 2:
                ip = cols[0].get_text(strip=True)
                port = cols[1].get_text(strip=True)
                if ip.count('.') == 3 and port.isdigit():
                    proxy_pool.append(f"{ip}:{port}")

    return proxy_pool

# Exemple d'utilisation :
proxies = fetch_live_proxies()
print("\n[Infos] Proxy lists : OK")
print(f"[Infos] {len(proxies)} proxies loaded.")
print("[Infos] Rotate Circuits Proxy : Active!\n")

# 🔎 Affichage des proxies récupérés
print("[Debug] List of proxies:")
for index, proxy in enumerate(proxies, 1):
    print(f"  [{index}] {proxy}")
