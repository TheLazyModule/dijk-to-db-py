import os

from dotenv import load_dotenv

from db.db import Database
from utils.utils import read_to_graph


def config_env():
    env_mode = os.getenv('ENV', 'development')  # Default to 'production' if ENV mode is not set

    if env_mode == 'development':
        dotenv_file = '.env.development'
    else:
        dotenv_file = '.env'

    load_dotenv(dotenv_file)


def init_db(graph):
    db = Database(
        dbname=os.environ.get("PGDATABASE"),
        user=os.environ.get("PGUSER"),
        host=os.environ.get("PGHOST"),
        password=os.environ.get("PGPASSWORD"),
        sslmode='disable' if os.environ.get("ENV") == "development" else "require"
    )
    db.connect()
    db.insert_nodes_edges(graph=graph)
    db.execute_sql_file('data/category.sql')
    print("inserted into category table")
    db.insert_shapefile_to_postgis(shapefile_path='data/place/places.shp', table_name='place')
    db.insert_shapefile_to_postgis(shapefile_path='data/building/building.shp', table_name='building')
    print("inserted into building and place tables")
    db.execute_sql_file('data/building/building_images.sql')
    print("Inserted building images")
    db.execute_sql_file('data/classroom/classroom.sql')
    print("Inserted classroom data")


def run():
    config_env()
    if os.path.exists("paths.geojson"):
        graph = read_to_graph(file_name="paths.geojson", should_densify_segments=True, distance=2)
        init_db(graph=graph)
        # graph.nodes_to_csv()
    else:
        print("❌ File not found!\nExiting...")
