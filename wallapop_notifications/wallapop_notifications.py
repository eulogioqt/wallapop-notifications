from utils import log, Sleep

from .wallapop_scraper import WallapopScraper

class WallapopNotifications:
    def __init__(self, driver_path, topic, headless=False, verbose_sleep=False):
        self.driver_path = driver_path
        self.topic = topic
        self.verbose_sleep = verbose_sleep
        self.seen_items = []

        self.running = True
        self.wallapop_scraper = WallapopScraper(driver_path, topic, headless, verbose_sleep)

    def stop(self):
        self.running = False
        Sleep.stop()
        # self.wallapop_scraper.close() # Estudiar si es necesario

    def run(self, callback):
        try:
            while self.running:
                wallapop_items = self.wallapop_scraper.get_items()

                if self.wallapop_scraper.scraps_done > 1:
                    log(f"Scrap realizado, analizando {len(wallapop_items)} items.")

                    new_items = 0
                    for item in wallapop_items:
                        if item not in self.seen_items:
                            self.seen_items.append(item) 
                            log(f"Nuevo ítem encontrado (número {len(self.seen_items)}): {item}")
                            callback(item)
                            new_items += 1
                        else:
                            break

                    log(f"Se han encontrado {new_items} nuevos items.")
                else:
                    self.seen_items = wallapop_items[1:]
                    log(f"Memoria inicializada con los {len(self.seen_items)} últimos items. A partir de ahora se le notificará de cada nuevo item publicado.")
                
                Sleep.sleep(60, "Nueva petición en %ds", verbose=self.verbose_sleep)
        finally:
            log("Wallapop Notifications detenido.")
