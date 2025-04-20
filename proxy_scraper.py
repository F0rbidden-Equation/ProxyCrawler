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
            if len(cols) >= 5:
                ip = cols[0].get_text(strip=True)
                port = cols[1].get_text(strip=True)
                protocols = cols[2].get_text(strip=True)
                # Récupération du pays depuis le div
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

# Exemple d'utilisation
proxies = fetch_live_proxies()

print("\n[Infos] Proxy lists : OK")
print(f"[Infos] {len(proxies)} proxies loaded.")
print("[Infos] Rotate Circuits Proxy : Active!\n")

# 🔎 Affichage test
for index, proxy in enumerate(proxies, 1):
    print(f"[{index}] {proxy['ip']}:{proxy['port']} - {proxy['protocol']} - {proxy['country']}")
