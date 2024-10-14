from utils import log

from .websocket_server import WebSocketServer
from .http_server import HTTPServer
from .websocket_thread_mixer import WebSocketThreadMixer
from wallapop_notifications import WallapopNotifications

class WallapopWebserver:

    def __init__(self, driver_path, topic, headless=False):
        self.driver_path = driver_path
        self.topic = topic
        self.headless = headless

        self.wallapop_notifications = WallapopNotifications(driver_path, topic, self.notification_callback, headless)
        self.websocket_server = WebSocketServer(self.on_message, self.on_user_connect, self.on_user_disconnect)
        self.http_server = HTTPServer("0.0.0.0", 8080)

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
        websocket_thread_mixer = WebSocketThreadMixer(self.websocket_server, self.wallapop_notifications, self.http_server)
        websocket_thread_mixer.run()