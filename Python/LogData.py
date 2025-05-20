from datetime import datetime
from threading import Thread
from queue import Queue
import time

log_start_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
LOG_FILE = f"{log_start_time}_voo_dados.txt"

log_queue = Queue()

def log_worker(filename):
    while True:
        json_data = log_queue.get()
        if json_data is None: 
            break
        timestamp = datetime.utcnow().isoformat()
        try:
            with open(filename, "a") as f:
                f.write(f"{timestamp} | {json_data}\n")
        except Exception as e:
            print(f"[ERRO] Falha ao gravar dados no ficheiro: {e}")
        log_queue.task_done()

log_thread = Thread(target=log_worker, args=(LOG_FILE,), daemon=True)
log_thread.start()

def log_data_to_file(json_data):
    log_queue.put(json_data)
