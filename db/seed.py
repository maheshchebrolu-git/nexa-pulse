import os
import random
from pathlib import Path
from dotenv import load_dotenv
import psycopg2
import geopandas as gpd
from faker import Faker
import json


PROJECT_ROOT = Path(__file__).parent.parent
env_path = PROJECT_ROOT / ".env"
load_dotenv(dotenv_path=env_path)
ROADS_PATH = PROJECT_ROOT / "db" / "data" / "tiger_sf_roads" / "tl_2025_06075_roads.shp"

conn = psycopg2.connect(
    host=os.getenv("POSTGRES_HOST"),
    port=os.getenv("POSTGRES_PORT"),
    dbname=os.getenv("POSTGRES_DB"),
    user=os.getenv("POSTGRES_USER"),
    password=os.getenv("POSTGRES_PASSWORD")
)
cursor = conn.cursor()
cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'nexa';")
print("Tables found:", cursor.fetchall())

print("Loading SF road network...")
roads = gpd.read_file(ROADS_PATH)
roads = roads.to_crs(epsg=4326)
print(f"Loaded {len(roads)} road segments (CRS: {roads.crs}).")

def random_point_on_road(roads_gdf):
    road = roads_gdf.sample(1).iloc[0]
    line = road.geometry
    fraction = random.random()
    point = line.interpolate(fraction, normalized=True)
    return point.y, point.x  

fake = Faker()

VEHICLE_MAKES_MODELS = [
    ("Toyota", "Camry"), ("Honda", "Accord"), ("Toyota", "Prius"),
    ("Tesla", "Model 3"), ("Honda", "Civic"), ("Ford", "Fusion"),
    ("Hyundai", "Elantra"), ("Nissan", "Altima")
]
VEHICLE_COLORS = ["black", "white", "silver", "gray", "blue", "red"]

def generate_driver_metadata():
    make, model = random.choice(VEHICLE_MAKES_MODELS)
    return {
        "name": fake.name(),
        "phone": fake.phone_number(),
        "vehicle_make": make,
        "vehicle_model": model,
        "vehicle_color": random.choice(VEHICLE_COLORS),
        "license_plate": fake.license_plate(),
        "rating": round(random.uniform(4.0, 5.0), 2)
    }

STATUSES = ['available', 'on_trip', 'offline']
NUM_DRIVERS = 200

for _ in range(NUM_DRIVERS):
    lat, lng = random_point_on_road(roads)
    status = random.choice(STATUSES)
    metadata = json.dumps(generate_driver_metadata())
    cursor.execute(
        """
        INSERT INTO nexa.drivers (location, status, metadata)
        VALUES (ST_SetSRID(ST_MakePoint(%s, %s), 4326), %s, %s)
        """,
        (lng, lat, status, metadata)
    )

conn.commit()
print(f"Inserted {NUM_DRIVERS} drivers, road-snapped to real SF streets, with metadata")

cursor.close()
conn.close()