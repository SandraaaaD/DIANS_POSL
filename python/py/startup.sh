#!/bin/bash
# Стартување на FastAPI апликација со Gunicorn + Uvicorn workers

# Опционално: активирање на virtual environment, ако го користиш
# source /home/site/wwwroot/.venv/bin/activate

# Стартување на апликацијата
gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app --bind 0.0.0.0:8000