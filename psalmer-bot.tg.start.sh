#!/bin/bash

echo
echo Check and install packages...
echo

pip install -r requirements.txt

echo
echo "PYTHONPATH: $PYTHONPATH"
echo

echo "Starting the Telegram bot..."
echo

python3 ./psalmer/bots/telegram/psalmer-bot.py

