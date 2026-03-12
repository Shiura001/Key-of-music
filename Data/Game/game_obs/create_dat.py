import pickle

#from Data.Game.game_obs.ofuscar_dat import guardar_progreso
from ofuscar_dat import *
# Los datos que querés persistir
datos_a_guardar = {
    "usuario": "none",
    "monedas": 0
}

# Usamos tu función (podés cambiar el 123 por una clave más compleja)
guardar_progreso(datos_a_guardar, password=124)
print("¡Progreso de Panther IA guardado con éxito!")