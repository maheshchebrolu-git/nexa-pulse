import os
from pathlib import Path
from dotenv import load_dotenv
import psycopg2

env_path = Path(__file__).parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

conn = psycopg2.connect(
    host=os.getenv("POSTGRES_HOST"),
    port=os.getenv("POSTGRES_PORT"),
    dbname=os.getenv("POSTGRES_DB"),
    user=os.getenv("POSTGRES_USER"),
    password=os.getenv("POSTGRES_PASSWORD")
)

cursor = conn.cursor()
cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'nexa';")
results = cursor.fetchall()
print(results)
cursor.close()
conn.close()
