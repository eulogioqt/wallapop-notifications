import datetime
import asyncio
import websockets
import webbrowser
import os

from queue import Queue
from utils import log
from wallapop_notifications import WallapopNotifications

clients = set()
queue = Queue()
stop_event = asyncio.Event()

driver_path = "D:/Programas/ChromeDriver/chromedriver.exe"
wallapop_notifications = WallapopNotifications(driver_path, "raspberry", headless=False)

def callback_function(item):
    queue.put(item)

def stop_program():
    if not stop_event.is_set():
        stop_event.set()
        wallapop_notifications.stop()

async def handler(websocket, path):
    clients.add(websocket)
    log("Cliente conectado")
    await send_message(websocket, "Conectado correctamente. Serás notificado de los nuevos productos en wallapop.")

    try:
        async for message in websocket:
            log(f"Mensaje recibido: {message}")
            if message == "STOP":
                stop_program()
                break

        log("Cliente desconectado") # Aqui se ejecuta si es una desconexion normal, si no, no ejecuta esta parte
    except Exception as e:
        log(f"Error en el cliente: {e}")
    finally:
        clients.remove(websocket)

async def broadcast():
    try:
        while not stop_event.is_set():
            if not queue.empty():
                if clients:
                    item = queue.get()
                    log(f"Enviando: {item}")

                    msg = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S") + ' ' + str(item) + ' <a href="' + item.link + '" target="_blank">link</a>'
                    await asyncio.gather(*[send_message(client, msg) for client in clients]) # LO SABIA RETURNS EXCEPTION
                    await asyncio.sleep(0)
            else:
                await asyncio.sleep(1)
    finally:
        log("Bucle Broadcast detenido.")

async def send_message(client, message):
    try:
        await client.send(str(message))
    except Exception as e:
        log(f"Error al enviar mensaje al cliente: {e}")

async def websocket_server():
    log("Iniciando servidor WebSocket...")
    try:
        async with websockets.serve(handler, "localhost", 8765):
            log("Servidor WebSocket en ejecución en ws://localhost:8765")
            await stop_event.wait()
    finally:
        for client in clients:
            await client.close()

        log("Servidor WebSocket detenido.")

async def run_wallapop_notifications(wallapop_notifications):
    loop = asyncio.get_event_loop()  # Esta tarea SI en un hilo separado
    await loop.run_in_executor(None, wallapop_notifications.run, callback_function)

async def main():    
    websocket_task = asyncio.create_task(websocket_server())
    broadcast_task = asyncio.create_task(broadcast())
    wallapop_task = asyncio.create_task(run_wallapop_notifications(wallapop_notifications))

    try:
        await asyncio.gather(websocket_task, broadcast_task, wallapop_task)
    finally:
        stop_program()

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.abspath(__file__))
    relative_path = 'wallapop_webclient/index.html'
    file_path = os.path.join(base_dir, relative_path)

    url = f'file://{file_path}'
    webbrowser.open(url)

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        log("El programa fue interrumpido manualmente.")
    except Exception as e:
        log(f"El programa fue detenido debido a un error: {e}")
    finally:
        log("Programa finalizado.")

