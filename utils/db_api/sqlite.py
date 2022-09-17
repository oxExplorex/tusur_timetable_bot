from utils.times import get_time_now
import sqlite3

path_to_db = "data/db.db"

def get_user(user_id):
    with sqlite3.connect(path_to_db) as db:
        return db.execute("SELECT * FROM users WHERE user_id = ?", (user_id,)).fetchall()


def create_users(user_id):
    with sqlite3.connect(path_to_db) as db:
        db.execute("INSERT INTO users (user_id) VALUES (?);", (user_id,))


def select_fast_answer_by_request(find_text: str):
    with sqlite3.connect(path_to_db) as db:
        return db.execute("SELECT * FROM fast_answer WHERE find_text = ?;", (find_text,)).fetchall()

def select_fast_answer_by_url(url: str):
    with sqlite3.connect(path_to_db) as db:
        return db.execute("SELECT * FROM fast_answer WHERE end_url = ?;", (url,)).fetchall()

def create_fast_answer_by_request(find_text="", result="", end_url=""):
    with sqlite3.connect(path_to_db) as db:
        db.execute("INSERT INTO fast_answer (find_text, result, end_url, datetime) VALUES (?, ?, ?, ?);",
                   (find_text, result, end_url, get_time_now(),))


def update_fast_answer_information(url: str, find_text="", result=""):
    with sqlite3.connect(path_to_db) as db:
        db.execute("""
            UPDATE fast_answer SET 
                find_text = ?,
                result = ?,
                datetime = ?
            WHERE end_url = ?; """, (find_text, result, get_time_now(), url,))

def update_fast_answer_information_by_text(find_text: str, url="", result=""):
    with sqlite3.connect(path_to_db) as db:
        db.execute("""
            UPDATE fast_answer SET 
                end_url = ?,
                result = ?,
                datetime = ?
            WHERE find_text = ?; """, (url, result, get_time_now(), find_text,))
