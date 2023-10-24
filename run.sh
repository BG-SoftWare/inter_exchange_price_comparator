#!/usr/bin/env bash
source venv/bin/activate
cd price_updaters
python3 truncate_price.py
screen -dmS price_screener_worker python3 binance.py
screen -dmS price_screener_worker python3 gate.py
while [ screen -list | grep -q "price_screener_worker" ]
do
  sleep 1
done
python3 price_comparator.py