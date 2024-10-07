import time
from datetime import datetime

def log(msg):
    current_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    print(f"[{current_time}] {msg}")

def sleep(seconds, msg=None, verbose=True):
    for i in range(seconds):
        if msg and verbose:
            log(msg.replace("%d", str(seconds - i)))

        time.sleep(1)