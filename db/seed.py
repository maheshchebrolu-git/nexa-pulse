import os
import random
import json
from pathlib import Path

from dotenv import load_dotenv
import psycopg2
import geopandas as gpd
from faker import Faker
import networkx as nx
from scipy.spatial import distance

# Setup: locate and load .env regardless of where this script is run from
PROJECT_ROOT = Path(__file__).parent.parent
env_path = PROJECT_ROOT / ".env"
load_dotenv(dotenv_path=env_path)
ROADS_PATH = PROJECT_ROOT / "db" / "data" / "tiger_sf_roads" / "tl_2025_06075_roads.shp"

# Database connection
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

# Load real San Francisco road data (TIGER/Line, US Census Bureau)
# Reprojected from native NAD83 (EPSG:4269) to WGS84 (EPSG:4326) to match
# the SRID used throughout the Nexa Pulse schema.
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

# Drivers
VEHICLE_MAKES_MODELS = [
    ("Toyota", "Camry"), ("Honda", "Accord"), ("Toyota", "Prius"),
    ("Tesla", "Model 3"), ("Honda", "Civic"), ("Ford", "Fusion"),
    ("Hyundai", "Elantra"), ("Nissan", "Altima")
]
VEHICLE_COLORS = ["black", "white", "silver", "gray", "blue", "red"]
STATUSES = ['available', 'on_trip', 'offline']
NUM_DRIVERS = 200


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


def seed_drivers():
#    To clear existing drivers before seeding, uncomment the following line:
#    cursor.execute("TRUNCATE TABLE nexa.drivers CASCADE;")

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
    print(f"Inserted {NUM_DRIVERS} drivers, road-snapped to real SF streets, with metadata.")

# Demand Zones
DEMAND_ZONES = [
    {
        "name": "Financial District",
        "zone_type": "commercial",
        "points": [(-122.4036, 37.7946), (-122.3958, 37.7937), (-122.3928, 37.7895), (-122.3994, 37.7903), (-122.4036, 37.7946)],
    },
    {
        "name": "SOMA",
        "zone_type": "commercial",
        "points": [(-122.4115, 37.7857), (-122.3975, 37.7825), (-122.3990, 37.7745), (-122.4140, 37.7775), (-122.4115, 37.7857)],
    },
    {
        "name": "Mission",
        "zone_type": "residential_nightlife",
        "points": [(-122.4234, 37.7647), (-122.4090, 37.7647), (-122.4090, 37.7480), (-122.4234, 37.7480), (-122.4234, 37.7647)],
    },
    {
        "name": "Marina / Fisherman's Wharf",
        "zone_type": "tourist",
        "points": [(-122.4450, 37.8060), (-122.4100, 37.8080), (-122.4070, 37.7990), (-122.4420, 37.7970), (-122.4450, 37.8060)],
    },
    {
        "name": "Inner Sunset",
        "zone_type": "residential",
        "points": [(-122.4720, 37.7660), (-122.4630, 37.7660), (-122.4630, 37.7580), (-122.4720, 37.7580), (-122.4720, 37.7660)],
    },
    {
        "name": "Castro",
        "zone_type": "residential_commercial",
        "points": [(-122.4380, 37.7650), (-122.4280, 37.7650), (-122.4280, 37.7550), (-122.4380, 37.7550), (-122.4380, 37.7650)],
    },
    {
        "name": "West Portal",
        "zone_type": "residential",
        "points": [(-122.4680, 37.7420), (-122.4620, 37.7420), (-122.4620, 37.7360), (-122.4680, 37.7360), (-122.4680, 37.7420)],
    },
]

def seed_demand_zones():
#    To clear existing demand zones before seeding, uncomment the following line:
#    cursor.execute("TRUNCATE TABLE nexa.demand_zones CASCADE;")

    for zone in DEMAND_ZONES:
        points_sql = ", ".join([f"ST_MakePoint({lng}, {lat})" for lng, lat in zone["points"]])
        metadata = json.dumps({"zone_type": zone["zone_type"]})
        request_count = random.randint(20, 60)

        cursor.execute(
            f"""
            INSERT INTO nexa.demand_zones (name, area, request_count, metadata)
            VALUES (%s, ST_SetSRID(ST_MakePolygon(ST_MakeLine(ARRAY[{points_sql}])), 4326), %s, %s)
            """,
            (zone["name"], request_count, metadata)
        )

    conn.commit()
    print(f"Inserted {len(DEMAND_ZONES)} demand zones.")

def build_road_graph(roads_gdf):
    G = nx.Graph()
    for _, row in roads_gdf.iterrows():
        line = row.geometry
        coords = list(line.coords)
        for i in range(len(coords) - 1):
            start = coords[i]
            end = coords[i + 1]
            dist = distance.euclidean(start, end)
            G.add_edge(start, end, weight=dist)
    return G

def nearest_node(G, lat, lng):
    point = (lng, lat)
    nodes = list(G.nodes)
    nearest = min(nodes, key=lambda node: distance.euclidean(node, point))
    return nearest

def compute_shortest_path(G, pickup_lat, pickup_lng, dropoff_lat, dropoff_lng):
    start = nearest_node(G, pickup_lat, pickup_lng)
    end = nearest_node(G, dropoff_lat, dropoff_lng)
    try:
        path = nx.shortest_path(G, source=start, target=end, weight='weight')
        return path
    except nx.NetworkXNoPath:
        return None

def path_to_linestring_sql(path):
    points_sql = ", ".join([f"ST_MakePoint({lng}, {lat})" for lng, lat in path])
    return f"ST_SetSRID(ST_MakeLine(ARRAY[{points_sql}]), 4326)"

NUM_TRIPS = 150
# Track drivers currently on trips to avoid double-booking
drivers_currently_on_trip = set() 

def seed_trips():
#    To clear existing trips before seeding, uncomment the following line:
#    cursor.execute("TRUNCATE TABLE nexa.trips CASCADE;")
    cursor.execute("SELECT id FROM nexa.drivers;")
    driver_ids = [row[0] for row in cursor.fetchall()]
    road_graph = build_road_graph(roads)
    for _ in range(NUM_TRIPS):
        pickup_lat, pickup_lng = random_point_on_road(roads)
        dropoff_lat, dropoff_lng = random_point_on_road(roads)
        route = compute_shortest_path(
            road_graph, pickup_lat, pickup_lng, dropoff_lat, dropoff_lng
            )
        has_driver = random.random() < 0.8
        driver_id = None
        status = 'requested'

        if has_driver:
            status = random.choice(['in_progress', 'completed', 'completed', 'completed', 'cancelled'])
            if status == 'in_progress':
                available_drivers = [d for d in driver_ids if d not in drivers_currently_on_trip]
                if available_drivers:
                    driver_id = random.choice(available_drivers)
                    drivers_currently_on_trip.add(driver_id)
                else:
                    driver_id = None
                    status = 'requested'
            else:
                driver_id = random.choice(driver_ids)

        route_sql = path_to_linestring_sql(route) if route else "NULL"
        fare_estimate = round(random.uniform(8.0, 45.0), 2)
        metadata = json.dumps({"fare_estimate_usd": fare_estimate})

        cursor.execute(
            f"""
            INSERT INTO nexa.trips (driver_id, pickup_location, dropoff_location, route, status, metadata)
            VALUES (
            %s, 
            ST_SetSRID(ST_MakePoint(%s,%s), 4326), 
            ST_SetSRID(ST_MakePoint(%s, %s), 4326), 
            {route_sql}, 
            %s, 
            %s)
            """,
            (driver_id, pickup_lng, pickup_lat, dropoff_lng, dropoff_lat, status, metadata)
        )
    
    conn.commit()
    print(f"Inserted {NUM_TRIPS} trips.")


if __name__ == "__main__":
    seed_drivers()  
    seed_demand_zones() 
    seed_trips()

    cursor.close()
    conn.close()