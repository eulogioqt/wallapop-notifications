from utils import log

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

from .wallapop_item import WallapopItem

class WallapopScraper:
    def __init__(self, driver_path, topic, headless=False):
        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--disable-software-rasterizer")
        chrome_options.add_argument("--log-level=3")  # Desactiva los mensajes de log de nivel INFO y ERROR
        chrome_options.add_argument("--silent")  # Hace que Chrome sea silencioso
        chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])  # Desactiva los logs de DevTools
        if headless:
            chrome_options.add_argument("--headless") 

        self.driver = webdriver.Chrome(service=Service(driver_path), options=chrome_options)
        self.url = f"https://es.wallapop.com/app/search?filters_source=quick_filters&keywords={topic}&order_by=newest" 
        self.scraps_done = 0

    def get_item_title(self, web_item):
        return web_item.find_element(By.CSS_SELECTOR, ".ItemCard__title").text
    
    def get_item_price(self, web_item):
        return web_item.find_element(By.CSS_SELECTOR, ".ItemCard__price").text

    def get_item_link(self, web_item):
        return web_item.get_attribute("href")

    def get_item(self, web_item):
        title = self.get_item_title(web_item)
        price = self.get_item_price(web_item)
        link = self.get_item_link(web_item)

        return WallapopItem(title, price, link)

    def get_items(self):
        self.driver.get(self.url)

        wallapop_items = []
        try: # No debería salir después de la primera vez
            accept_button = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Aceptar todo')]")))
            accept_button.click() # Aceptar Cookies
        except Exception:
            pass

        try: # No debería salir después de la primera vez
            for i in range(3):  # Hacer clic en "Saltar" hasta que se quite
                skip_button = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//walla-button[contains(@class, 'TooltipWrapper__skip')]")))
                skip_button.click()
        except Exception:
            pass

        try:
            web_items = self.driver.find_elements(By.CSS_SELECTOR, ".ItemCardList__item")
            for web_item in web_items:
                wallapop_item = self.get_item(web_item)
                wallapop_items.append(wallapop_item)
        except Exception:
            log("ERROR AL OBTENER ITEMS")

        self.scraps_done = self.scraps_done + 1

        return wallapop_items
