import threading
import webbrowser

from utils import log

from .websocket_server import WebsocketServer
from wallapop_notifications import WallapopNotifications

class WallapopWebserver:

    def __init__(self, client_url, driver_path, topic, headless=False):
        self.client_url = client_url
        self.driver_path = driver_path
        self.topic = topic
        self.headless = headless

        self.wallapop_notifications = WallapopNotifications(driver_path, topic, headless=headless)
        self.websocket_server = WebsocketServer(self.on_message, self.on_user_connect, self.on_user_disconnect)

    def on_message(self, msg):
        response = None

        if msg == "STOP":
            self.websocket_server.stop_program()
        elif msg == "TEST":
            response = "Working fine"
        
        return response

    def on_user_connect(self, client_ip, client_port):
        log(f"Cliente conectado ({client_ip}:{client_port}) (Conexiones: {self.websocket_server.get_connection_count()})")

        return "Conectado correctamente. Serás notificado de los nuevos productos en wallapop."
    
    def on_user_disconnect(self, client_ip, client_port):
        log(f"Cliente desconectado ({client_ip}:{client_port}) (Conexiones: {self.websocket_server.get_connection_count()})")

    def notification_callback(self, wallapop_item):
        log("Nuevo item recibido. Notificando en la web: " + str(wallapop_item))

        self.websocket_server.broadcast_message(str(wallapop_item) + ' <a href="' + wallapop_item.link + '" target="_blank">AQUI</a>')

    def run(self): # Hacer objeto wrapper para los threads "WebsocketThreadMixer" 
        webbrowser.open(self.client_url)

        wallapop_nnotifications_thread = threading.Thread(target=self.wallapop_notifications.run, args=(self.notification_callback,), daemon=False)
        wallapop_nnotifications_thread.start()

        try:
            self.websocket_server.run()
        finally:
            log("Websocket Server finalizado.")

            self.wallapop_notifications.stop()
            wallapop_nnotifications_thread.join()

            log("Programa terminado.")