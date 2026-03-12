from fastapi import FastAPI
from pydantic import BaseModel
import database
import hashlib
import json

app = FastAPI()

SECRET = "clave_ultra_secreta"

# ------------------------
# Modelo de score
# ------------------------
class Score(BaseModel):
    player: str
    song: str
    combo: int
    score: int
    signature: str

# ------------------------
# Funciones anti-cheat
# ------------------------
def sign_data(data: dict):
    copy = data.copy()
    del copy["signature"]

    text = json.dumps(copy, sort_keys=True) + SECRET
    return hashlib.sha256(text.encode()).hexdigest()


def verify_signature(data: dict):
    expected = sign_data(data)
    return expected == data["signature"]


def calculate_score(combo):
    # lógica simple
    return combo


# ------------------------
# Endpoints
# ------------------------
@app.post("/submit_score")
def submit_score(data: Score):

    data_dict = data.dict()

    # 1️⃣ verificar firma
    if not verify_signature(data_dict):
        return {"error": "datos manipulados"}


    # 3️⃣ validar límites
    if data.combo < 0:
        return {"error": "valores imposibles"}

    # 4️⃣ guardar score
    database.add_score(data.player, data.song, data.combo, data.score)

    return {
        "message": "score guardado correctamente",
        "score": data.score
    }


@app.get("/leaderboard/{song}")
def leaderboard(song: str):

    scores = database.get_leaderboard(song)

    result = [
        {"player": player, "combo": combo, "score": score}
        for player, combo, score in scores
    ]

    return result


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server_secure:app", host="127.0.0.1", port=8000, reload=True)