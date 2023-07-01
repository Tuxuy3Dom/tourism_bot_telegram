# tourism_bot_telegram
Creating this repository is your own choice of topic for a project at a university. University of Information Technology and Management

## Creating a virtual environment and activation 

Creating standart virtual environment in Python
```bash
python -m venv .venv
```

Activations standart virtual environment in Python
```bash
.venv\Scripts\activate
```

#### After doing this, we can install the libraries and frameworks we need for the project.

## Installation
Use the package manager [pip](https://pip.pypa.io/en/stable/) to install aiogram.

Installation Guide [aiogram](https://docs.aiogram.dev/en/latest/install.html)
```bash
pip install aiogram
```

Installing dotenv for read file .env [python-dotenv](https://pypi.org/project/python-dotenv/)
```bash
pip install python-dotenv
```

## After cloning my repositorium 

Create file .env
```bash
TOKEN='YOUR_ACCESS_TOKEN'
```

## Used imports the project 

```python
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
import os, logging
```

## Start run project

```bash
python main.py
```

## Used commands of the bot in telegram

### User commands:

Getting started communication with the bot:
```bash
/start
```

We start the state of the machine for creating a user profil
```bash
/create_profil
```

This command displays all available commands for the user
```bash
/help
```

This command connects to an external applicaion 
```bash
/open
```

This command displays all available tourist places in the database 
```bash
/all_places
```

This text get your profil 
```bash
Profil
```

This text delete your profil 
```bash
Delete profile
```

### Admin commands:

This command gives you access to the admin panel, where you need to be an admin of that group [Tourism Group](https://t.me/tourisms_group) to get access.
```bash
/moderator
```

#### After getting to the admin panel:

This allows you to add a new tourist spot to the database.
```bash
/new_place
```

We're removing a tourist spot from the database.
```bash
/delete
```




