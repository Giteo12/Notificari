#  Itch.io Game Tracker & Wishlist Manager

Acest script Python este un instrument automatizat pentru monitorizarea jocurilor de pe platforma **itch.io**. Acesta urmărește prețurile, actualizările și descrierile jocurilor, oferind notificări desktop și un jurnal detaliat al modificărilor.

##  Funcționalități Principală
- **Monitorizare Automată**: Verifică periodic listele de jocuri (Bibliotecă și Wishlist).
- **Notificări Desktop**: Te alertează instant când un preț se schimbă sau apare o reducere.
- **Bază de Date Locală**: Salvează starea jocurilor în format CSV (`biblioteca_jocuri.csv`).
- **Jurnal de Istoric**: Înregistrează fiecare modificare detectată în `istoric_detaliat.csv`.
- **Interfață Curată**: Afișează datele sub formă de tabel organizat direct în consolă.


##  Explicația Funcțiilor

### `extrage_date_joc(url)`
Accesează pagina jocului și extrage informațiile esențiale (Titlu, Preț, Data Update, Descriere) folosind tehnici de Web Scraping.

### `verifica_jocuri()`
Funcția centrală care:
1. Compară datele actuale de pe site cu cele salvate în baza de date locală.
2. Identifică modificările de preț sau de conținut.
3. Declanșează notificările desktop dacă apar schimbări importante.

### `sterge_din_wishlist(url)`
Funcție utilitară care permite eliminarea unui joc din monitorizare prin furnizarea URL-ului său. Aceasta rescrie fișierul de bază de date, eliminând intrarea respectivă.

### `afisare_eleganta()`
Printează în terminal un tabel formatat estetic, aliniind coloanele pentru o citire ușoară a titlurilor, prețurilor și a tipului de monitorizare.

### `initializeaza_fisiere()`
Se asigură că fișierele de date (`.csv`) există la pornirea programului, creându-le cu antetul corect dacă acestea lipsesc.

##  Mod de Utilizare

1. Editează listele `BIBLIOTECA_URLS` și `WISHLIST_URLS` din cod cu link-urile dorite.
2. Rulează programul:
   ```bash
   python nume_fisier_tau.py
   ```
3. Programul va efectua o scanare completă, va afișa tabelul și va repeta procesul automat la fiecare 60 de minute.
