FROM python:3.11-slim

WORKDIR /app

# 1. Инсталирај dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 2. Копирај апликација
COPY py/ ./py

# 3. Копирај wait-for-it
#COPY wait-for-it.sh /app/wait-for-it.sh
#RUN chmod +x /app/wait-for-it.sh

ENV PYTHONPATH=/app/py
#
## 4. Команда за стартување: чека Postgres, потоа стартува filtri.py и Uvicorn
#CMD ["/bin/bash", "/app/start.sh"]

# Копирај го start.sh
COPY start.sh /app/start.sh
RUN chmod +x /app/start.sh

# CMD сега само стартува start.sh
CMD ["/bin/bash", "/app/start.sh"]
