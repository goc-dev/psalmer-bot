cp .env.template .env

mcedit .env

export PYTHONPATH=/workspaces/plsamer-bot/psalmer

pip install -r requirements.txt

python3 bots/telegram/psalmer-bot.py