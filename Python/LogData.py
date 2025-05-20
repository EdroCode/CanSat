from datetime import datetime

LOG_FILE = "voo_dados.txt"

def log_data_to_file(json_data, filename=LOG_FILE):
    timestamp = datetime.utcnow().isoformat()
    try:
        with open(filename, "a") as f:
            f.write(f"{timestamp} | {json_data}\n")
    except Exception as e:
        print(f"[ERRO] Falha ao gravar dados no ficheiro: {e}")
