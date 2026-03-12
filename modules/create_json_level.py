import json

def guardar_json(self):
    # Guardamos la lista en un archivo llamado 'mi_nivel.json'
    with open('mi_nivel.json', 'w') as archivo:
        json.dump(self.mis_notas_grabadas, archivo, indent=4)