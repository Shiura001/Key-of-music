import os
import pickle

def guardar_progreso(datos, password=123):
    # Serializamos el objeto a bytes
    datos_binarios = pickle.dumps(datos)
    
    # Aplicamos un XOR simple (u otra encriptación) para ofuscar
    datos_ofuscados = bytearray(b ^ (password % 256) for b in datos_binarios)
    
    with open("Data/Game/game_obs/progreso.dat", "wb") as f:
        f.write(datos_ofuscados)

# Para leerlo hacés el proceso inverso
def cargar_progreso(password=123):
    ruta = "Data/Game/game_obs/progreso.dat"
    
    # 1. Verificamos si existe y si NO está vacío (tamaño > 0)
    if not os.path.exists(ruta) or os.path.getsize(ruta) == 0:
        print("Archivo vacío o inexistente. Generando datos por defecto...")
        return {"usuario": "Dylan", "monedas": 0}

    try:
        with open(ruta, "rb") as f:
            datos_leidos = f.read()
            
        # Revertimos la ofuscación
        datos_originales = bytearray(b ^ (password % 256) for b in datos_leidos)
        
        # 2. Verificamos que lo desofuscado no esté vacío
        if not datos_originales:
            return {"usuario": "none", "monedas": 0}
            
        return pickle.loads(datos_originales)
        
    except Exception as e:
        print(f"Error técnico al deserializar: {e}")
        # Si falla, devolvemos un diccionario seguro para que el juego no crashee
        return {"usuario": "none", "monedas": 0}

