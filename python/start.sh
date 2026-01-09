#!/bin/bash
# Чека PostgreSQL да е готов
/app/wait-for-it.sh my_postgres:5432 --timeout=60 --strict -- echo "Postgres е достапен"

# Стартува Python updater во background
python -m py.filtri &

# Стартува Uvicorn
uvicorn py.main:app --host 0.0.0.0 --port 8000
