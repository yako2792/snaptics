#!/bin/bash
cd /home/user/Documents/snaptics 
source .venv/bin/activate
#flet run --port 8000 --web -a resources/assets -m src.main
python -m src.main
