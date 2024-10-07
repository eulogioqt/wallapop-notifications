from wallapop_notifications import WallapopNotifications

driver_path = "D:/Programas/ChromeDriver/chromedriver.exe"
topic = "raspberry"

def callback_function(item):
    print("AAAAAAAA UN NUEVO ITEM!!! " + str(item))

wallapop_notifications = WallapopNotifications(driver_path, topic)
wallapop_notifications.run(callback_function)