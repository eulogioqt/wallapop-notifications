from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time

# Define la ruta a chromedriver.exe
driver_path = 'D:/Programas/ChromeDriver/chromedriver.exe'  # Cambia por la ruta correcta de tu sistema

# Opciones para el navegador (headless)
chrome_options = Options()
chrome_options.add_argument("--headless")  # Ejecutar en modo headless (sin ventana gráfica)

# Crea el objeto Service con el driver_path
service = Service(driver_path)

# Inicia el driver de Chrome con las opciones de headless
driver = webdriver.Chrome(service=service, options=chrome_options)

# Cargar la página
url = "https://es.wallapop.com/app/search?filters_source=quick_filters&keywords=raspberry&longitude=-3.69196&latitude=40.41956&order_by=newest"  # Cambia por la URL real
driver.get(url)

try:
    # Esperar hasta que el botón "Aceptar todo" esté presente en la página y hacer clic en él
    accept_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Aceptar todo')]"))
    )
    accept_button.click()

    for _ in range(3):  # Hacer clic en "Saltar" 3 veces
        # Esperar hasta que el botón "Saltar" esté presente y hacer clic en él
        skip_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//walla-button[contains(@class, 'TooltipWrapper__skip')]"))
        )

        skip_button.click()

    items = driver.find_elements(By.CSS_SELECTOR, ".ItemCardList__item")

    # Mostrar el número de elementos encontrados
    print(f"Se encontraron {len(items)} elementos de tipo 'tsl-public-item-card'.")

    # Opcional: Mostrar los textos o atributos de los elementos
    i = 1
    for item in items:
        title = item.find_element(By.CSS_SELECTOR, ".ItemCard__title").text
        price = item.find_element(By.CSS_SELECTOR, ".ItemCard__price").text
        link = item.get_attribute("href")  # Obtener el enlace del item
        print(f"{i}. Título: {title} | Precio: {price} | Enlace: {link}")

        i = i+1

finally:
    # Cerrar el navegador
    driver.quit()
