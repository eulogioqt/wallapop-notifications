from wallapop_webserver import WallapopWebserver

driver_path = "D:/Programas/ChromeDriver/chromedriver.exe"
topic = "raspberry"

wallapop_webserver = WallapopWebserver(driver_path, topic, headless=True)
wallapop_webserver.run()