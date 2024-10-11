import os
from wallapop_webserver import WallapopWebserver

client_url = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'wallapop_webclient/index.html')
driver_path = "D:/Programas/ChromeDriver/chromedriver.exe"
topic = "raspberry"

wallapop_webserver = WallapopWebserver(client_url, driver_path, topic)
wallapop_webserver.run()
