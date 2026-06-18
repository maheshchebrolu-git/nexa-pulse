-- Enable the core extensions
CREATE EXTENSION IF NOT EXISTS postgis;
CREATE EXTENSION IF NOT EXISTS vector;

-- Namespace for all Nexa Pulse tables
CREATE SCHEMA IF NOT EXISTS nexa;

---
-- CORE TABLES
---

-- 1. Drivers: live operational state of each driver
CREATE TABLE IF NOT EXISTS nexa.drivers (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    location geometry(Point, 4326),
    status VARCHAR(20) NOT NULL DEFAULT 'offline'
        CHECK (status IN ('available', 'on_trip', 'offline')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    metadata JSONB
);

-- 2. Demand_zones: geographical areas with high demand, used for strategic insights and driver positioning.
CREATE TABLE IF NOT EXISTS nexa.demand_zones (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(50) NOT NULL,
    area geometry(Polygon, 4326) NOT NULL,
    request_count INTEGER NOT NULL DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    metadata JSONB
);

-- 3. Trips: historical and real-time trip data
----- Single-table design: requests and active trips share one table via status.
----- Could split into ride_requests + trips in production; kept single for simplicity.
CREATE TABLE IF NOT EXISTS nexa.trips (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    driver_id UUID REFERENCES nexa.drivers(id), -- null means trip requested but not yet matched with a driver
    pickup_location geometry(Point, 4326) NOT NULL,
    dropoff_location geometry(Point, 4326) NOT NULL,
    route geometry(LineString, 4326),
    status VARCHAR(25) NOT NULL DEFAULT 'requested'
        CHECK (status IN ('requested', 'in_progress', 'completed', 'cancelled')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    metadata JSONB
);

-- 4. Policy_docs: store policy documents for vector search and retrieval.
CREATE TABLE IF NOT EXISTS nexa.policy_docs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    content TEXT NOT NULL,
    embedding VECTOR(384),
    metadata JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

---
-- PERFORMANCE ARCHITECTURE: INDEXES
---

-- Spatial Optimization (GiST)

-- 1. Drivers Table 
-- Index on location for spatial queries.
CREATE INDEX IF NOT EXISTS idx_drivers_location 
ON nexa.drivers USING GIST (location);

-- Partial spatial index: only available drivers, indexed by location.
-- Serves the dominant query "available drivers near a point."
CREATE INDEX IF NOT EXISTS idx_drivers_available_location 
ON nexa.drivers USING GIST (location) WHERE status = 'available';

-- 2. Demand_zones Table
-- Indexing the area for spatial queries.
CREATE INDEX IF NOT EXISTS idx_demand_zones_area
ON nexa.demand_zones USING GIST (area);

-- 3. Trips Table
-- Partial spatial index: only active trips, indexed by pickup location.
-- Active-vs-historical split: completed trips (the bulk) aren't queried spatially.
CREATE INDEX IF NOT EXISTS idx_trips_active_pickup
ON nexa.trips USING GIST (pickup_location)
WHERE status IN ('requested', 'in_progress');

-- B-tree on driver_id for looking up a driver's trips (including history).
CREATE INDEX IF NOT EXISTS idx_trips_driver_id
ON nexa.trips (driver_id);

-- 4. Policy_docs Table
-- Indexing embedding for vector search
CREATE INDEX IF NOT EXISTS idx_policy_docs_embedding
ON nexa.policy_docs USING hnsw (embedding vector_cosine_ops);

