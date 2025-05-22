from datetime import datetime
from threading import Thread
from queue import Queue
import time
import os

log_queue = Queue()
LOG_FILE = None 
PATH = None

def set_file():

    global LOG_FILE , PATH
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    folder_path = f"/home/pi/{timestamp}"
    PATH = folder_path
    os.makedirs(folder_path, exist_ok=True)
    
    LOG_FILE = os.path.join(folder_path, f"{timestamp}_voo_dados.txt")

def log_worker():
    while True:
        json_data = log_queue.get()
        if json_data is None: 
            break
        timestamp = datetime.utcnow().isoformat()
        try:
            with open(LOG_FILE, "a") as f:
                f.write(f"{timestamp} | {json_data}\n")
        except Exception as e:
            print(f"[ERRO] Falha ao gravar dados no ficheiro: {e}")
        log_queue.task_done()

def start_logging():
    set_file()
    thread = Thread(target=log_worker, daemon=True)
    thread.start()
    return thread

def log_data_to_file(json_data):
    log_queue.put(json_data)

