import requests
from bs4 import BeautifulSoup
from plyer import notification
import csv
import os
import time


BIBLIOTECA_URLS = ["https://itch.io"]
WISHLIST_URLS = ["https://itch.io"]

DB_FILE = 'biblioteca_jocuri.csv'
HISTORY_FILE = 'istoric_detaliat.csv'

def initializeaza_fisiere():
    if not os.path.exists(DB_FILE):
        with open(DB_FILE, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['url', 'titlu', 'pret', 'update_data', 'descriere', 'tip']) 

    if not os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['data_ora', 'titlu', 'eveniment', 'pret_vechi', 'pret_nou', 'descriere_veche'])

def scrie_in_istoric(titlu, eveniment, p_vechi, p_nou, d_veche):
    with open(HISTORY_FILE, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([time.strftime('%Y-%m-%d %H:%M:%S'), titlu, eveniment, p_vechi, p_nou, d_veche])

def verifica_jocuri():
    initializeaza_fisiere()
    
    date_existente = {}
    if os.path.exists(DB_FILE):
        with open(DB_FILE, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                date_existente[row['url']] = row

    toate_jocurile = [(u, "Biblioteca") for u in BIBLIOTECA_URLS] + [(u, "Wishlist") for u in WISHLIST_URLS]
    biblioteca_noua = []

    for url, tip in toate_jocurile:
        try:
            print(f"Verific ({tip}): {url}")
            res = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=10)
            soup = BeautifulSoup(res.text, 'html.parser')

            
            titlu = soup.find('h1', class_='game_title').get_text(strip=True) if soup.find('h1', class_='game_title') else "Necunoscut"
            pret_nou = (soup.find('span', class_='price') or soup.find('div', class_='buy_row')).get_text(strip=True) if (soup.find('span', class_='price') or soup.find('div', class_='buy_row')) else "Free"
            update_nou = soup.find('abbr', title=True)['title'] if soup.find('abbr', title=True) else "N/A"
            desc_noua = soup.find('div', class_='formatted_description').get_text(strip=True)[:150] + "..." if soup.find('div', class_='formatted_description') else "N/A"

            if url in date_existente:
                date_vechi = date_existente[url]
                
                
                if pret_nou != date_vechi['pret']:
                    prefix = " WISHLIST REDUCERE:" if tip == "Wishlist" else "Preț schimbat:"
                    notification.notify(title=titlu, message=f"{prefix} {date_vechi['pret']} -> {pret_nou}", timeout=10)
                    scrie_in_istoric(titlu, "Schimbare Pret", date_vechi['pret'], pret_nou, date_vechi['descriere'])
                
                if desc_noua != date_vechi['descriere']:
                    scrie_in_istoric(titlu, "Update Descriere", pret_nou, pret_nou, date_vechi['descriere'])
                    print(f" [!] Descrierea pentru {titlu} s-a schimbat.")

            else:
                
                scrie_in_istoric(titlu, f"Adaugat in {tip}", "-", pret_nou, "Prima scanare")

            biblioteca_noua.append([url, titlu, pret_nou, update_nou, desc_noua, tip])

        except Exception as e:
            print(f" Eroare la {url}: {e}")

   
    with open(DB_FILE, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['url', 'titlu', 'pret', 'update_data', 'descriere', 'tip'])
        writer.writerows(biblioteca_noua)


while True:
    verifica_jocuri()
    print("\nVerificare completă. Următoarea peste o oră.")
    time.sleep(3600)