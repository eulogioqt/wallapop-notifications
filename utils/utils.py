import time
import socket

from datetime import datetime

def log(msg):
    current_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    print(f"[{current_time}] {msg}")

def get_local_ip():
    ip = "127.0.0.1"
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip

class Sleep:
    _running = True

    @classmethod
    def sleep(cls, seconds, msg=None, verbose=True):
        for i in range(seconds):
            if not cls._running:
                break

            if msg and verbose:
                log(msg.replace("%d", str(seconds - i))) 

            time.sleep(1) 

    @classmethod
    def stop(cls):
        cls._running = False
