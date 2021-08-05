######
# Code for handling coonnections to our MongoDB
######

# List of fields can be found here: https://docs.mongoengine.org/apireference.html#mongoengine.fields.StringField

from mongoengine import connect, Document, ListField, StringField, URLField, IntField

# Connect to our MongoServer
server_file = open("server.txt", "r")
server = server_file.read()

def db_connect():
    connect(db="tutorial", host=server, port=27017)

class Character(Document):
    discord_name = StringField(required=True, max_length=20)
    name = StringField(required=True, max_length=20)
    avatar_url = URLField(required=True)
    level = IntField(required=True, min_value=0, max_value=99)
    exp = IntField(required=True, min_value=0, max_value=9999)
    char_id = IntField(db_field='id', required=True, min_value=0, max_value=256)
    hp = IntField(required=True, min_value=0, max_value=256)
    max_hp = IntField(required=True, min_value=0, max_value=256)
    sp = IntField(required=True, min_value=0, max_value=256)
    max_sp = IntField(required=True, min_value=0, max_value=256)
    power = IntField(required=True, min_value=0, max_value=256)
    shield = IntField(required=True, min_value=0, max_value=256)
    spd = IntField(required=True, min_value=0, max_value=256)
    lk = IntField(required=True, min_value=0, max_value=256)
    inventory = ListField(StringField(max_length=99))

def create_character(user, name, avatar, id, stat_bonus):
    # Create a new default character with the passed unique things
    character = Character()
    character.discord_name = user
    character.name = name
    character.avatar_url = avatar
    character.char_id = id
    character.level = 1
    character.exp = 0
    character.hp = 10
    character.max_hp = 10
    character.sp = 5
    character.max_sp = 5
    character.power = 1
    character.shield = 1
    character.spd = 1
    character.lk = 0
    character.inventory = ["[Nothing]"]

    if (stat_bonus == "hp"):
        character.hp = 15
        character.max_hp = 15
    elif (stat_bonus == "sp"):
        character.sp = 10
        character.max_sp = 10
    elif (stat_bonus == "power"):
        character.power = 3
    elif (stat_bonus == "shield"):
        character.shield = 3
    elif (stat_bonus == "spd"):
        character.spd = 3
    elif (stat_bonus == "lk"):
        character.lk = 1

    # Save the new character to the DB
    character.save()

    return character

def get_chars(user):
    # Make a counter
    count = 0

    # Make a list of character names
    characters = []

    # Loop through the characters and find the characters associated with the Discord user
    for doc in Character.objects(discord_name=user):
        count += 1
        characters.append(doc)

    return count, characters

def get_total_char():
    count = 0

    for doc in Character.objects():
        count += 1

    return count