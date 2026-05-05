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

def extrage_date_joc(url):
    try:
        res = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=10)
        soup = BeautifulSoup(res.text, 'html.parser')
        titlu = soup.find('h1', class_='game_title').get_text(strip=True) if soup.find('h1', class_='game_title') else "Necunoscut"
        pret = (soup.find('span', class_='price') or soup.find('div', class_='buy_row')).get_text(strip=True) if (soup.find('span', class_='price') or soup.find('div', class_='buy_row')) else "Free"
        update = soup.find('abbr', title=True)['title'] if soup.find('abbr', title=True) else "N/A"
        desc = soup.find('div', class_='formatted_description').get_text(strip=True)[:50] + "..." if soup.find('div', class_='formatted_description') else "N/A"
        return titlu, pret, update, desc
    except:
        return "Eroare Conexiune", "N/A", "N/A", "N/A"


def sterge_din_wishlist(url_target):
    """Elimină un joc din fișierul CSV folosind URL-ul"""
    if not os.path.exists(DB_FILE):
        return
    
    jocuri_ramase = []
    gasit = False
    
    with open(DB_FILE, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        for row in reader:
            if row['url'] == url_target and row['tip'] == 'Wishlist':
                gasit = True
                continue 
            jocuri_ramase.append(row)
    
    if gasit:
        with open(DB_FILE, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(jocuri_ramase)
        print(f"✅ Jocul {url_target} a fost eliminat cu succes.")
    else:
        print("❌ Jocul nu a fost găsit în Wishlist.")

def afisare_eleganta():
    """Printează conținutul bazei de date sub formă de tabel curat"""
    if not os.path.exists(DB_FILE):
        print("Baza de date goală.")
        return

    print("\n" + "="*90)
    print(f"{'TIP':<12} | {'TITLU':<30} | {'PRET':<12} | {'ULTIMUL UPDATE'}")
    print("-" * 90)

    with open(DB_FILE, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            titlu_scurt = (row['titlu'][:27] + '...') if len(row['titlu']) > 27 else row['titlu']
            print(f"{row['tip']:<12} | {titlu_scurt:<30} | {row['pret']:<12} | {row['update_data']}")
    print("="*90 + "\n")



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
        print(f"🔍 Scanare {tip}: {url}")
        titlu, pret_nou, update_nou, desc_noua = extrage_date_joc(url)
       
        biblioteca_noua.append([url, titlu, pret_nou, update_nou, desc_noua, tip])

    
    with open(DB_FILE, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['url', 'titlu', 'pret', 'update_data', 'descriere', 'tip'])
        writer.writerows(biblioteca_noua)
    
    
    afisare_eleganta()
