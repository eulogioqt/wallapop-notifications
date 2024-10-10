import time
from datetime import datetime

def log(msg):
    current_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    print(f"[{current_time}] {msg}")

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
