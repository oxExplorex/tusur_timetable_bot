import sqlite3

path_to_db = "data/db.db"

def get_user(user_id):
    with sqlite3.connect(path_to_db) as db:
        return db.execute("SELECT * FROM users WHERE user_id = ?", (user_id,)).fetchall()


def create_users(user_id):
    with sqlite3.connect(path_to_db) as db:
        db.execute("INSERT INTO users (user_id) VALUES (?);", (user_id,))
