#!/usr/bin/env bash
source venv/bin/activate
python3 whitelist_generator.py
python3 main.py
screen -dmS price_comparators python3 price_comparator_cex.py