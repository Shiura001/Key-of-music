import requests
import hashlib
import json

# URL pública de ngrok o local
SERVER_URL = "https://uniteable-ashlie-unprudentially.ngrok-free.dev"

# Clave secreta (debe coincidir con el servidor)
SECRET = "clave_ultra_secreta"

# ------------------------
# Función para generar la firma
# ------------------------
def sign_score(player, song, combo, score):
    data = {
        "player": player,
        "song": song,
        "combo": combo,
        "score": score,
        "signature": ""  # temporal, se elimina para la firma
    }

    # Crear hash SHA256
    copy = data.copy()
    del copy["signature"]
    text = json.dumps(copy, sort_keys=True) + SECRET
    signature = hashlib.sha256(text.encode()).hexdigest()
    data["signature"] = signature

    return data

# ------------------------
# Función para enviar score
# ------------------------
def submit_score(player, song, combo, score):
    data = sign_score(player, song, combo, score)
    response = requests.post(f"{SERVER_URL}/submit_score", json=data)
    return response.json()



# -----------------------------
# Obtener leaderboard
# -----------------------------
def get_leaderboard(song):
    response = requests.get(f"{SERVER_URL}/leaderboard/{song}")
    return response.json()

# ------------------------
# Ejemplo de uso
# ------------------------


#submit_score("dan", "level_3", 999999, 999999)
import sqlite3 # o el driver que uses en tu proyecto

def limpiar_tablas():
    # Asegurate de que el nombre del archivo coincida (¿scores.db o database.db?)
    conn = sqlite3.connect('scores.db') 
    cursor = conn.cursor()
    
    # Aquí va el nombre de la TABLA, no de los campos
    tablas = ["scores"] 
    
    try:
        for tabla in tablas:
            # DELETE borra las filas, pero la estructura queda
            cursor.execute(f"DELETE FROM {tabla}")
            
            # Esto resetea los IDs para que el próximo sea 1
            cursor.execute(f"DELETE FROM sqlite_sequence WHERE name='{tabla}'")
            
        conn.commit()
        print("¡Leaderboard de Nite Software reseteada!")
    except Exception as e:
        # Aquí verás el error real, como "no such table" si el nombre está mal
        print(f"Error al limpiar: {e}")
    finally:
        conn.close()
    
    
    
#limpiar_tablas()