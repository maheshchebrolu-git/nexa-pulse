FROM postgis/postgis:16-3.4

RUN apt-get update && \
    apt-get install -y postgresql-16-pgvector=0.8.2-1.pgdg11+1 && \
    rm -rf /var/lib/apt/lists/*