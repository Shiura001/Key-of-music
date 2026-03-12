import sqlite3

# Conexión global
conn = sqlite3.connect("scores.db", check_same_thread=False)
cursor = conn.cursor()

# Tabla para scores
cursor.execute("""
CREATE TABLE IF NOT EXISTS scores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    player TEXT,
    song TEXT,
    combo INTEGER,
    score INTEGER
)
""")
conn.commit()


def add_score(player, song, combo, score):
    cursor.execute(
        "INSERT INTO scores (player, song, combo, score) VALUES (?, ?, ?, ?)",
        (player, song, combo, score)
    )
    conn.commit()


def get_leaderboard(song):
    cursor.execute("""
        SELECT player, combo, score
        FROM scores
        WHERE song = ?
        ORDER BY score DESC
        LIMIT 10
    """, (song,))
    return cursor.fetchall()