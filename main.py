from wallapop_webserver import WallapopWebserver
import os

driver_path = "D:/Programas/ChromeDriver/chromedriver.exe"
topic = "raspberry"
client_url = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'wallapop_webclient/index.html')

wallapop_webserver = WallapopWebserver(client_url, driver_path, topic, headless=False)
wallapop_webserver.run()