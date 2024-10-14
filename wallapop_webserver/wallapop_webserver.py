import threading
import webbrowser

from utils import log, get_local_ip

from .websocket_server import WebsocketServer
from .http_server import HTTPServer
from wallapop_notifications import WallapopNotifications

class WallapopWebserver:

    def __init__(self, driver_path, topic, headless=False):
        self.driver_path = driver_path
        self.topic = topic
        self.headless = headless

        self.wallapop_notifications = WallapopNotifications(driver_path, topic, headless=headless)
        self.websocket_server = WebsocketServer(self.on_message, self.on_user_connect, self.on_user_disconnect)
        self.http_server = HTTPServer(host="0.0.0.0", port=8080)

    def on_message(self, msg):
        log(f"Mensaje recibido: {msg}")
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
        log(f"Nuevo item recibido. Notificando en la web: {str(wallapop_item)}")

        self.websocket_server.broadcast_message(str(wallapop_item) + ' <a href="' + wallapop_item.link + '" target="_blank">AQUI</a>')

    def run(self):
        webbrowser.open(f"http://{get_local_ip()}:8080")

        wallapop_notifications_thread = threading.Thread(target=self.wallapop_notifications.run, args=(self.notification_callback,), daemon=False)
        wallapop_notifications_thread.start()

        http_server_thread = threading.Thread(target=self.http_server.start, daemon=False)
        http_server_thread.start()

        try:
            self.websocket_server.run()
        finally:
            log("Websocket Server finalizado.")

            self.wallapop_notifications.stop()
            wallapop_notifications_thread.join()
            log("Wallapop Notifications finalizado.")

            self.http_server.stop()
            http_server_thread.join()
            log("HTTP Server finalizado.")

            log("Programa terminado.")