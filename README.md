# Itch.io Game Tracker & Notifier

Acest script Python monitorizează jocurile de pe platforma **itch.io**, urmărind modificările de preț și actualizările descrierilor. Oferă notificări desktop în timp real și păstrează un istoric detaliat al schimbărilor.

##  Funcționalități principale

1.  **Monitorizare Automată**: Verifică periodic (implicit la fiecare oră) o listă de URL-uri definită pentru Bibliotecă și Wishlist.
2.  **Sistem de Notificări**: Trimite notificări de tip Windows/macOS/Linux folosind `plyer` atunci când:
    *   Un preț scade sau se modifică.
    *   Un joc din Wishlist intră la reducere.
3.  **Bază de Date CSV**:
    *   `biblioteca_jocuri.csv`: Stochează starea actuală a jocurilor monitorizate.
    *   `istoric_detaliat.csv`: Înregistrează cronologic orice schimbare detectată (istoric prețuri, update-uri de descriere).
4.  **Web Scraping**: Extrage automat titlul, prețul, data ultimei actualizări și primele 150 de caractere din descriere.
5.  **Notificare la Cerere**: Include o funcție specială pentru a verifica rapid un joc prin introducerea unui link manual.



### Funcția de Notificare Manuală
Dacă vrei să primești o notificare instantanee pentru un joc anume fără a-l adăuga în baza de date pe termen lung, poți apela:
```python
notifica_joc_manual("https://itch.io")
```

##  Structura Fișierelor
*   `main.py`: Scriptul principal.
*   `biblioteca_jocuri.csv`: Cache-ul local pentru a compara prețurile noi cu cele vechi.
*   `istoric_detaliat.csv`: Jurnalul tuturor evenimentelor detectate de la prima rulare.

##  Note
Scriptul folosește un `User-Agent` pentru a evita blocarea cererilor și are un mecanism de tratare a erorilor (try-except) pentru a preveni oprirea scriptului în cazul în care un link este invalid.
