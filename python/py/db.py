import asyncpg

DB_CONFIG = {
    "host": "my_postgres",
    "port": 5432,
    "user": "postgres",
    "password": "postgres",
    "database": "dians_baza",
}

# DB_CONFIG = { 'host': 'das-db-2026.postgres.database.azure.com',
#               'port': 5432,
#               'user': 'postgres',
#               'password': 'sd7589F!nk!',
#               'database': 'example_db',
#               }

async def get_pool():
    return await asyncpg.create_pool(**DB_CONFIG)