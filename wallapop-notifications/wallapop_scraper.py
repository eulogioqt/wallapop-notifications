import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

from wallapop_item import WallapopItem

class WallapopScraper:
    def __init__(self, driver_path, url):
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Ejecutar en modo headless (sin ventana gráfica)

        self.driver = webdriver.Chrome(service=Service(driver_path), options=chrome_options)
        self.url = url

    def get_item(self, web_item):
        title = web_item.find_element(By.CSS_SELECTOR, ".ItemCard__title").text
        price = web_item.find_element(By.CSS_SELECTOR, ".ItemCard__price").text
        link = web_item.get_attribute("href")  # Obtener el enlace del item

        return WallapopItem(title, price, link)

    def get_items(self):
        self.driver.get(self.url)

        wallapop_items = []
        try:
            accept_button = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Aceptar todo')]")))
            accept_button.click() # Aceptar Cookies

            for _ in range(3):  # Hacer clic en "Saltar" 3 veces
                skip_button = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//walla-button[contains(@class, 'TooltipWrapper__skip')]")))
                skip_button.click()

            web_items = self.driver.find_elements(By.CSS_SELECTOR, ".ItemCardList__item")
            for web_item in web_items:
                wallapop_item = self.get_item(web_item)
                wallapop_items.append(wallapop_item)

        except Exception:
            print("Ha habido algún error obteniendo los items")
            
        self.driver.quit()
        return wallapop_items
