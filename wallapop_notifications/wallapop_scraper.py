from utils import log, Sleep

from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

from .wallapop_item import WallapopItem

class WallapopScraper:
    def __init__(self, driver_path, topic, headless=False, verbose_sleep=False):
        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--disable-software-rasterizer")
        chrome_options.add_argument("--log-level=3")  # Desactiva los mensajes de log de nivel INFO y ERROR
        chrome_options.add_argument("--silent")  # Hace que Chrome sea silencioso
        # chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])  # Bugea el cerrado de chrome driver
        if headless:
            chrome_options.add_argument("--headless") 

        self.driver = webdriver.Chrome(service=Service(driver_path), options=chrome_options)
        self.url = f"https://es.wallapop.com/app/search?filters_source=quick_filters&keywords={topic}&order_by=newest" 
        self.verbose_sleep = verbose_sleep
        self.scraps_done = 0

    def close(self):
        if self.driver:
            self.driver.quit()

    def do_get(self, url):
        self.driver.get(url)

    def click_accept_button(self):
        accept_button = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Aceptar todo')]")))
        accept_button.click()

    def click_skip_button(self):
        skip_button = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//walla-button[contains(@class, 'TooltipWrapper__skip')]")))
        skip_button.click()

    def get_wallapop_elements(self):
        return self.driver.find_elements(By.CSS_SELECTOR, ".ItemCardList__item")

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
        self.do_get(self.url)

        log(f"Iniciando scrap número {self.scraps_done + 1}...")

        wallapop_items = []
        if self.scraps_done == 0:
            try:
                self.click_accept_button()
                log("Click en Aceptar Todo")
            except WebDriverException:
                pass # No está el botón

            try:
                for i in range(3):
                    self.click_skip_button()
                    log(f"Click en Saltar ({i + 1}/3)")
            except WebDriverException:
                pass # No está el botón 
        else:
            Sleep.sleep(5, "Esperando a que carguen los items (%ds)", self.verbose_sleep)

        try:
            log("Buscando items...")
            web_items = self.get_wallapop_elements()
            for web_item in web_items:
                wallapop_item = self.get_item(web_item)
                if wallapop_item.is_empty():
                    log("Se ha detectado un item vacio")
                else:
                    wallapop_items.append(wallapop_item)
        except WebDriverException:
            log("ERROR: Se ha producido un problema al obtener items")

        self.scraps_done = self.scraps_done + 1

        return wallapop_items
