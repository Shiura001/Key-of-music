# run_server.py
import subprocess
import time
from threading import Thread
import uvicorn

PORT = 8000
FASTAPI_MODULE = "server_secure:app"
NGROK_COMMAND = ["ngrok", "http", str(PORT)]
WAIT_NGROK = 3

def start_fastapi():
    uvicorn.run(FASTAPI_MODULE, host="127.0.0.1", port=PORT, reload=True)

def start_ngrok():
    print("Arrancando ngrok...")
    subprocess.Popen(NGROK_COMMAND)
    time.sleep(WAIT_NGROK)
    print("Ngrok corriendo! Revisa la consola de ngrok para la URL pública.")

if __name__ == "__main__":
    Thread(target=start_ngrok).start()
    start_fastapi()