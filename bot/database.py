import hikari
import psycopg2
import os


# Class to represent our DB connection
class Database:
    def __init__(self):
        self._conn = None
        self._cursor = None
        self.open()

    @property
    def conn(self):
        return self._conn

    @property
    def cursor(self):
        return self._cursor

    def open(self):
        # Connect to the Luigi Bot Database for user EXP, Levels, and Birthdays
        self._conn = psycopg2.connect(os.getenv("DATABASE_URL"))
        self._cursor = self._conn.cursor()

    def close(self):
        self._cursor.close()
        self._conn.close()

    def restart(self):
        self.close()
        self.open()

    def add_user(self, user_id):
        try:
            self.cursor.execute(f"INSERT INTO users(user_id, level, exp) VALUES({user_id}, 0, 1)")
            self._conn.commit()
        except:
            self.restart()
            raise Exception("Something went wrong adding the user to the DB")

    def fetch_user(self, user_id):
        try:
            self.cursor.execute(f"SELECT * from users WHERE user_id = {user_id}")
            return self.cursor.fetchone()
        except:
            self.restart()
            raise Exception("Something went wrong fetching the user")

    def fetch_users(self):
        try:
            self.cursor.execute(f"SELECT * FROM users")
            return self.cursor.fetchall()
        except:
            self.restart()
            raise Exception("Something went wrong fetching the users")

    def fetch_exp(self, user_id):
        try:
            self.cursor.execute(f"SELECT exp FROM users WHERE user_id = {user_id}")
            return self.cursor.fetchone()
        except:
            self.restart()
            raise Exception("Something went wrong fetching the user's exp")

    def set_exp(self, user_id, amount):
        try:
            self.cursor.execute(f"UPDATE users SET exp = {amount} WHERE user_id = {user_id}")
            self._conn.commit()
        except:
            self.restart()
            raise Exception("Something went wrong updating the user's exp")

    def fetch_level(self, user_id):
        try:
            self.cursor.execute(f"SELECT level FROM users WHERE user_id = {user_id}")
            return self.cursor.fetchone()
        except:
            self.restart()
            raise Exception("Something went wrong fetching the user's level")

    def set_level(self, user_id, level):
        try:
            self.cursor.execute(f"UPDATE users SET level = {level} WHERE user_id = {user_id}")
            self._conn.commit()
        except:
            self.restart()
            raise Exception("Something went wrong updating the user's level")

    def fetch_leaderboard(self):
        try:
            self.cursor.execute(f"SELECT user_id, level, exp FROM users ORDER BY exp DESC")
            return self.cursor.fetchall()
        except:
            self.restart()
            raise Exception("Something went wrong fetching the leaderboard")

    def set_birthday(self, user_id, day, month, year):
        try:
            self.cursor.execute(f"UPDATE users SET birthday='{year}-{month}-{day}' WHERE user_id={user_id}")
            self._conn.commit()
        except:
            self.restart()
            raise Exception("Something went wrong updating the user's birthday")
