import asyncio
import websockets

from queue import Queue
from utils import log

class WebsocketServer:

    def __init__(self, on_message):
        self.on_message = on_message

        self.clients = set()
        self.queue = Queue()
        self.stop_event = asyncio.Event()

    def run(self):
        try: 
            asyncio.run(self.main())
        except KeyboardInterrupt: pass
        except Exception: pass
        finally: 
            log("Wallapop Server detenido.")

    def broadcast_message(self, msg):
        self.queue.put(msg)

    def stop_program(self):
        if not self.stop_event.is_set():
            self.stop_event.set()

    async def handler(self, websocket, path):
        self.clients.add(websocket)
        log("Cliente conectado")
        await self.send_message(websocket, "Conectado correctamente. Serás notificado de los nuevos productos en wallapop.")

        try:
            async for message in websocket:
                log(f"Mensaje recibido: {message}")
                response = self.on_message(message)
                if response is not None:
                    await self.send_message(websocket, response)

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
                        msg = self.queue.get()

                        await asyncio.gather(*[self.send_message(client, msg) for client in self.clients]) # LO SABIA RETURNS EXCEPTION
                        await asyncio.sleep(0)
                else:
                    await asyncio.sleep(1)
        finally:
            log("Tarea Broadcast detenida.")

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

            log("Tarea WebSocket detenida.")

    async def main(self):    
        websocket_task = asyncio.create_task(self.websocket_server())
        broadcast_task = asyncio.create_task(self.broadcast())

        try:
            await asyncio.gather(websocket_task, broadcast_task)
        finally:
            self.stop_program()