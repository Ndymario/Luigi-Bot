# Luigi Bot

[Discord Server Link](https://discord.gg/wz8jzp3czd)

Luigi Bot is a Discord bot made to add some games inside of Discord using Message Components as input.

## Features

- Games for you and your server members to play
    Currently, there is an RPG Game that features questing and a level system
- MongoDB database for storing user content long term for if the bot must go offline

## Installation

If you'd like to add Luigi Bot to your server, [click here](https://discord.com/oauth2/authorize?client_id=421169985617002496&scope=bot+applications.commands) for the bot invite link!

## Permissions
This bot needs a few permissions to run properly!
- Make Slash Commands
    All of the bot's commands are ran through these commands!
- Delete Messages
    Used for some games to keep the chat clean, as well as any moderation commands that involve deleting messages

## Development

Want to contribute? Here's how to get started!

Step 1:

Clone this repository to your machine (as you could have guessed ;p)

Optional Step 1.5:

If you would like to make a virtual environment for this instance as to keep these libraries separate from your main Python installation, follow these steps in your favorite Terminal app.

1. Go to the bot's folder
```sh
$ cd /path/to/Luigi-Bot
```
2. Create the Virtual Environment
```sh
$ python3 -m venv luigi-bot-env
```

3. Activate the Virtual Environment
```sh
# Linux/macOS
source luigi-bot-env/bin/activate

# Windows (PowerShell)
.\luigi-bot-env\Scripts\activate.ps1

# Windows (CMD)
.\luigi-bot-env\Scripts\activate.bat
```

Step 2:

Install the dependancies
```sh
# Linux/macOS
python3 -m pip install -r requirements.txt

# Windows
py -3 -m pip install -r requirements.txt
```

Step 3:

Follow [this tutorial](https://docs.mongodb.com/manual/installation/) to set up a local MongoDB database for connecting Luigi Bot to.

Step 4:

Add a file named "server.txt" in the root directory and add the text "localhost" inside of said txt file.

Step 5:

Add a file named "token.txt" to your own Application Bot Token.

## License

(Luigi Bot's License TBD)

This software uses a Discord Python Library, Discord Py Message Components Library, and MongoDB Engine; all of which are licensed under the MIT license. This project has not nor will not make any claims as to being the author of any of these pieces of software.

[Discord Python License][DPLL]

[Discord Py Message Components Library][MCLL]

[MongoDB Engine License][MDGEL]

## Copyright Notice
This project is not affiliated with Nintendo and does not claim to own "Luigi" or any other Nintendo Property.

[DPL]: <https://github.com/Pycord-Development/pycord>
[DPLL]: <https://github.com/Pycord-Development/pycord/blob/master/LICENSE>
[MCL]: <https://github.com/discord-py-slash-commands/discord-py-interactions>
[MCLL]: <https://github.com/discord-py-slash-commands/discord-py-interactions/blob/master/LICENSE>
[MDGE]: <http://mongoengine.org>
[MDGEL]: <https://github.com/MongoEngine/mongoengine/blob/master/LICENSE>
