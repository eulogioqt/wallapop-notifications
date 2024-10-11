import datetime
import asyncio
import websockets
import webbrowser
import signal

from queue import Queue
from utils import log
from wallapop_notifications import WallapopNotifications

class WallapopWebserver:

    def __init__(self, client_url, driver_path, topic, headless=False):
        self.clients = set()
        self.queue = Queue()
        self.stop_event = asyncio.Event()

        self.client_url = client_url
        self.driver_path = driver_path
        self.wallapop_notifications = WallapopNotifications(driver_path, topic, headless=headless)

        self.original_handler = signal.getsignal(signal.SIGINT)

    def run(self):
        signal.signal(signal.SIGINT, self.kill_handler)
        webbrowser.open(self.client_url)

        try: 
            asyncio.run(self.main())
        except KeyboardInterrupt: pass
        except Exception: pass
        finally: 
            log("Programa finalizado.")

    def kill_handler(self, signum, frame):
        log("CTRL + C detectado, deteniendo procesos...")
        if callable(self.original_handler):
            self.original_handler(signum, frame)

    def callback_function(self, item):
        self.queue.put(item)

    def stop_program(self):
        if not self.stop_event.is_set():
            self.stop_event.set()
            self.wallapop_notifications.stop()

    async def handler(self, websocket, path):
        self.clients.add(websocket)
        log("Cliente conectado")
        await self.send_message(websocket, "Conectado correctamente. Serás notificado de los nuevos productos en wallapop.")

        try:
            async for message in websocket:
                log(f"Mensaje recibido: {message}")
                if message == "STOP":
                    self.stop_program()
                    break

            log("Cliente desconectado") # Aqui se ejecuta si es una desconexion normal, si no, no ejecuta esta parte
        except Exception as e:
            log(f"Error en el cliente: {e}")
        finally:
            self.clients.remove(websocket)

    async def broadcast(self):
        try:
            while not self.stop_event.is_set():
                if not self.queue.empty():
                    if self.clients:
                        item = self.queue.get()
                        log(f"Enviando: {item}")

                        msg = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S") + ' ' + str(item) + ' <a href="' + item.link + '" target="_blank">link</a>'
                        await asyncio.gather(*[self.send_message(client, msg) for client in self.clients]) # LO SABIA RETURNS EXCEPTION
                        await asyncio.sleep(0)
                else:
                    await asyncio.sleep(1)
        finally:
            log("Bucle Broadcast detenido.")

    async def send_message(self, client, message):
        try:
            await client.send(str(message))
        except Exception as e:
            log(f"Error al enviar mensaje al cliente: {e}")

    async def websocket_server(self):
        log("Iniciando servidor WebSocket...")
        try:
            async with websockets.serve(self.handler, "localhost", 8765):
                log("Servidor WebSocket en ejecución en ws://localhost:8765")
                await self.stop_event.wait()
        finally:
            for client in self.clients:
                await client.close()

            log("Servidor WebSocket detenido.")

    async def run_wallapop_notifications(self, wallapop_notifications):
        loop = asyncio.get_event_loop()  # Esta tarea SI en un hilo separado
        await loop.run_in_executor(None, wallapop_notifications.run, self.callback_function)

    async def main(self):    
        websocket_task = asyncio.create_task(self.websocket_server())
        broadcast_task = asyncio.create_task(self.broadcast())
        wallapop_task = asyncio.create_task(self.run_wallapop_notifications(self.wallapop_notifications))

        try:
            await asyncio.gather(websocket_task, broadcast_task, wallapop_task)
        finally:
            self.stop_program()