from dataclasses import dataclass
from datetime import datetime
from pocketbase import PocketBase
from json import dumps
import hikari
import os


@dataclass
class User:
    id = int
    username = str
    exp = int
    level = int
    birthday = datetime
    hide_lvl_up = bool

    def __str__(self):
        return f"ID: {self.id}\nEXP: {self.exp}\nLVL: {self.level}\nBirthday: {self.birthday}\n" \
               f"Hide Lvl Up: {self.hide_lvl_up}"


# Class to represent our DB connection
class Database:
    def __init__(self):
        self.client = PocketBase("http://" + os.getenv("DATABASE_URL") + ":8090")
        self.max_level = 6
        self.max_exp = 50000
        self.exp_multiplier = 1

        self.level_table = {0: ("(No Rank)", range(0, 30)), 1: ("Super Mushroom", range(30, 490)),
                            2: ("Fire Flower", range(490, 2130)), 3: ("Blue Shell", range(2130, 6860)),
                            4: ("Super Star", range(6860, 22500)), 5: ("Big Star", range(22500, 50000)),
                            6: ("Mega Mushroom", range(500001, 999999999999999999))}

    def _get_pb_user(self, user_id: int):
        try:
            record = self.client.collection("users").get_list(1, 1, {"filter": f"user_id = {user_id}"}).items[0]

            user = User()
            user.id = record.id
            user.exp = record.exp
            user.level = record.level
            user.birthday = record.birthday
            user.hide_lvl_up = record.hide_lvl_up

            return user

        except IndexError:
            return None

    def _set_level(self, user: User, level: int):
        # This if is redundant dur to where this function is called, but it never hurt to make sure
        if user is None:
            return

        self.client.collection("users").update(str(user.id), {"level": level})

    def get_user(self, user_id: int):
        user = self._get_pb_user(user_id)

        if user is None:
            return None

        return user

    def add_user(self, user_id: int, username: str, exp: int = 0, level: int = 0, birthday=None):
        # Prevent duplicate user entries
        # if self._get_pb_user(user_id) is not None:
        #     raise ValueError(f"This user (id = {user_id}) already exists in the database!")

        self.client.collection("users").create({
            "user_id": user_id,
            "username": username,
            "exp": exp,
            "level": level,
            "birthday": birthday,
            "hide_lvl_up": False
        })

    def get_exp(self, user_id: int):
        user = self._get_pb_user(user_id)
        if user is None:
            return None

        return user.exp

    def set_exp(self, user_id: int, exp: int):
        user = self._get_pb_user(user_id)

        if user is None:
            return False

        self.client.collection("users").update(str(user.id), {"exp": exp})

        for level in self.level_table:
            if exp in self.level_table[level][1] and level != user.level:
                self._set_level(user, level)
                return True
            elif exp > self.max_exp and user.level != self.max_level:
                self._set_level(user, self.max_level)
                return True

    def get_level(self, user_id: int):
        user = self._get_pb_user(user_id)

        if user is None:
            return None

        return user.level

    def fetch_leaderboard(self, page: int):
        return self.client.collection("users").get_list(page, 10, {"sort": "-exp"}).items

    def get_birthday(self, user_id: int):
        user = self._get_pb_user(user_id)

        if user is None:
            return None

        return user.birthday

    def set_birthday(self, user_id: int, date):
        user = self._get_pb_user(user_id)
        if user is None:
            return None

        self.client.collection("users").update(str(user.id), {"birthday": str(date)})

    def get_lvl_announce_preference(self, user_id: int):
        user = self._get_pb_user(user_id)

        if user is None:
            return None

        return user.hide_lvl_up

    def set_lvl_announce_preference(self, user_id: int, preference: bool):
        user = self._get_pb_user(user_id)
        if user is None:
            return None

        self.client.collection("users").update(str(user.id), {"hide_lvl_up": preference})


if __name__ == "__main__":
    db = Database()

    print(db.get_user(306270307101179915))
