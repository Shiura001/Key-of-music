import hashlib
import pickle
import os

# --- TUS FUNCIONES DE SEGURIDAD (Copiadas de ofuscar_dat.py) ---
def generar_hash(datos_binarios, salt="Mi_Clave_Secreta_Pro"):
    """Genera la firma digital para el archivo"""
    return hashlib.sha256(datos_binarios + salt.encode()).hexdigest()

def guardar_progreso(datos, password=123):
    ruta_dat = "Data/Game/game_obs/progreso.dat"
    ruta_hash = "Data/Game/game_obs/progreso.hash"
    
    # 1. Serialización (Pickle)
    datos_binarios = pickle.dumps(datos)
    
    # 2. Ofuscación (XOR)
    datos_ofuscados = bytearray(b ^ (password % 256) for b in datos_binarios)
    
    # 3. Guardar el archivo binario (.dat)
    os.makedirs(os.path.dirname(ruta_dat), exist_ok=True)
    with open(ruta_dat, "wb") as f:
        f.write(datos_ofuscados)
    
    # 4. GENERAR Y GUARDAR LA FIRMA (.hash)
    # Importante: El hash se hace sobre los datos ya ofuscados
    firma = generar_hash(datos_ofuscados)
    with open(ruta_hash, "w") as f:
        f.write(firma)

# --- EJECUCIÓN DEL SCRIPT ---

# Los datos que querés persistir
datos_a_guardar = {
    "usuario": "Dylan",
    "monedas": 1000 # Aquí puedes ponerte las monedas que quieras para probar
}

# Usamos la función. 
# NOTA: El password debe ser el mismo que uses en el juego para cargar.
guardar_progreso(datos_a_guardar, password=124)

print("------------------------------------------")
print("¡Progreso de Panther IA guardado con éxito!")
print("Archivos generados: progreso.dat y progreso.hash")
print("------------------------------------------")