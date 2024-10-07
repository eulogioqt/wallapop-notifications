import time
from datetime import datetime
from wallapop_notifications import WallapopScraper

driver_path = "D:/Programas/ChromeDriver/chromedriver.exe"
topic = "raspberry"

wallapop_scraper = WallapopScraper(driver_path, topic)
seen_items = []

while True:
    try:
        wallapop_items = wallapop_scraper.get_items()
        print(f"Petición realizada correctamente. Analizando {len(wallapop_items)} items.")

        new_items = 0
        for item in wallapop_items:
            if item not in seen_items:
                seen_items.append(item) 
    
                index = len(seen_items)
                current_time = datetime.now().strftime("%d/%m/%Y %H:%M")
                
                print(f"[{current_time}] Nuevo ítem encontrado (número {index}): {item}")

                new_items = new_items + 1

        print(f"Se han encontrado {new_items} nuevos items.")

        for i in range(60):
            #print(f"Nueva petición en {60 - i}s")
            time.sleep(1)  # Frecuencia

    except Exception as e:
        print(f"Error: {e}")
        for i in range(5):
            #print(f"Reintentando en {5 - i}s")
            time.sleep(1)  # Frecuencia
