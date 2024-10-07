from utils import log, sleep
from wallapop_notifications import WallapopScraper

driver_path = "D:/Programas/ChromeDriver/chromedriver.exe"
topic = "raspberry"
verbose = False

wallapop_scraper = WallapopScraper(driver_path, topic)
seen_items = []

while True:
    try:
        wallapop_items = wallapop_scraper.get_items()
        log(f"Petición realizada correctamente. Analizando {len(wallapop_items)} items.")

        new_items = 0
        for item in wallapop_items:
            if item not in seen_items:
                seen_items.append(item) 
    
                index = len(seen_items)
                log(f"Nuevo ítem encontrado (número {index}): {item}")

                new_items = new_items + 1

        log(f"Se han encontrado {new_items} nuevos items.")
        sleep(60, "Nueva petición en %ds", verbose=verbose)

    except Exception as e:
        print(f"Error: {e}")
        sleep(5, "Reintentando en %ds", verbose=verbose)