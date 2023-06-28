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

## Usage 

```python
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
import os, logging
```