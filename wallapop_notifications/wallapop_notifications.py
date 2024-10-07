from utils import log, sleep

from .wallapop_scraper import WallapopScraper

class WallapopNotifications:

    def __init__(self, driver_path, topic, headless=False, verbose_sleep=False):
        self.driver_path = driver_path
        self.topic = topic
        self.verbose_sleep = verbose_sleep

        self.seen_items = []
        self.wallapop_scraper = WallapopScraper(driver_path, topic, headless, verbose_sleep)
    
    def run(self, callback):
        while True:
            try:
                wallapop_items = self.wallapop_scraper.get_items()

                if self.wallapop_scraper.scraps_done > 1:
                    log(f"Scrap realizado, analizando {len(wallapop_items)} items.")

                    new_items = 0
                    for item in wallapop_items:
                        if item not in seen_items:
                            seen_items.append(item) 
                            log(f"Nuevo ítem encontrado (número {len(seen_items)}): {item}")

                            callback(item)
                            new_items = new_items + 1
                        else: # Importante para que no detecte anuncios antiguos como nuevos
                            break

                    log(f"Se han encontrado {new_items} nuevos items.")

                else:
                    seen_items = wallapop_items
                    log(f"Memoria inicializada con los {len(seen_items)} últimos items. A partir de ahora se le notificará de cada nuevo item publicado.")
                
                sleep(60, "Nueva petición en %ds", verbose=self.verbose_sleep)
                
            except Exception as e:
                log(f"Error: {e}")
                sleep(5, "Reintentando en %ds", verbose=self.verbose_sleep)