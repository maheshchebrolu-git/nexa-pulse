-- Enable the core extensions
CREATE EXTENSION IF NOT EXISTS postgis;
CREATE EXTENSION IF NOT EXISTS vector;

-- Ensure an isolated schema for our agentic data structures
CREATE SCHEMA IF NOT EXISTS agent_memory;

-- 1. Documents Table: For unstructured knowledge, logs, and agent state narratives
CREATE TABLE IF NOT EXISTS agent_memory.documents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    content TEXT NOT NULL,
    metadata JSONB,
    embedding VECTOR(384),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 2. GIS Features Table: Core spatial asset management
CREATE TABLE IF NOT EXISTS agent_memory.gis_features (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    feature_name VARCHAR(255) NOT NULL,
    feature_type VARCHAR(50),
    geom GEOMETRY(Geometry, 4326),
    properties JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 3. Spatial Nodes Table: The discrete localized intelligence points
CREATE TABLE IF NOT EXISTS agent_memory.spatial_nodes (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    node_name VARCHAR(255) NOT NULL,
    metadata JSONB,
    location GEOMETRY(Point, 4326),
    embedding VECTOR(384),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

---
-- PERFORMANCE ARCHITECTURE: INDEXES
---

-- Spatial Optimization (GiST)
CREATE INDEX IF NOT EXISTS idx_gis_features_geom 
ON agent_memory.gis_features USING GIST (geom);

CREATE INDEX IF NOT EXISTS idx_spatial_nodes_location 
ON agent_memory.spatial_nodes USING GIST (location);

-- Semantic/Vector Optimization (HNSW)
-- Replacing the planned IVFFlat with HNSW for better recall at scale on Apple Silicon
CREATE INDEX IF NOT EXISTS idx_documents_embedding 
ON agent_memory.documents USING hnsw (embedding vector_cosine_ops);

CREATE INDEX IF NOT EXISTS idx_spatial_nodes_embedding 
ON agent_memory.spatial_nodes USING hnsw (embedding vector_cosine_ops);