import threading

from utils import log

class WebSocketThreadMixer:

    def __init__(self, websocket, *others):
        self.websocket = websocket
        self.others = others 
        self.threads = {}

    def run(self):
        for other in self.others: # Arrancamos hilos
            thread = threading.Thread(target=other.run, daemon=False)
            thread.start()

            self.threads[other.__class__.__name__] = thread
            
        try: self.websocket.run() # Principal websockets
        finally:
            log("WebSocketServer finalizado.")

            for other in self.others: # Paramos hilos
                other.stop()

            for th_name in self.threads.keys(): # Esperamos su muerte
                self.threads[th_name].join()
                log(th_name + " finalizado.")

            log("Programa terminado.")
