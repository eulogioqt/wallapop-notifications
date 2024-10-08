import asyncio
import websockets
import webbrowser
import os
from queue import Queue

from utils import log
from wallapop_notifications import WallapopNotifications

clients = set()
queue = Queue()

def callback_function(item):
    queue.put(item)

async def handler(websocket, path):
    clients.add(websocket)
    log("Cliente conectado")
    await send_message(websocket, "Conectado correctamente. Serás notificado de los nuevos productos en wallapop.")

    try:
        async for message in websocket:
            log(f"Mensaje recibido: {message}")
    except Exception as e:
        log(f"Error en el cliente: {e}")
    finally:
        log("Cliente desconectado")
        clients.remove(websocket)

async def broadcast():
    while True:
        if not queue.empty():
            if clients:  # Solo intenta enviar si hay clientes conectados
                item = queue.get()
                log(f"Enviando: {item}")

                await asyncio.gather(*[send_message(client, item) for client in clients])
                await asyncio.sleep(0)
        else:
            await asyncio.sleep(1)

async def send_message(client, message):
    try:
        await client.send(str(message))
    except Exception as e:
        log(f"Error al enviar mensaje al cliente: {e}")

async def websocket_server():
    log("Iniciando servidor WebSocket...")
    async with websockets.serve(handler, "localhost", 8765):
        log("Servidor WebSocket en ejecución en ws://localhost:8765")
        await asyncio.Future()  # Mantener el servidor corriendo indefinidamente

async def run_wallapop_notifications(wallapop_notifications):
    loop = asyncio.get_event_loop() # Usamos `run_in_executor` para ejecutar el bucle de Wallapop en un hilo separado
    await loop.run_in_executor(None, wallapop_notifications.run, callback_function)

async def main():
    driver_path = "D:/Programas/ChromeDriver/chromedriver.exe"
    wallapop_notifications = WallapopNotifications(driver_path, "raspberry", headless=True)
    
    websocket_task = asyncio.create_task(websocket_server())
    broadcast_task = asyncio.create_task(broadcast())
    wallapop_task = asyncio.create_task(run_wallapop_notifications(wallapop_notifications)) # VER QUE PASA PORQUE AUNQUE WALLAPOP TASK NO LO META EN GATHER FUNCIONAAAAA

    await asyncio.gather(websocket_task, broadcast_task, wallapop_task)

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.abspath(__file__))

    relative_path = 'wallapop_webclient/index.html'  # Ajusta esto según tu estructura de proyecto
    file_path = os.path.join(base_dir, relative_path)

    url = f'file://{file_path}'

    webbrowser.open(url)

    asyncio.run(main())
