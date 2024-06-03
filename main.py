from database.db import Database
from utils.utils import read_to_graph
import os
from dotenv import load_dotenv

mode = os.getenv('MODE', 'production')  # Default to 'production' if MODE is not set

if mode == 'development':
    dotenv_file = '.env.development'
else:
    dotenv_file = '.env'

# Load the environment variables from the chosen file
load_dotenv(dotenv_file)

if __name__ == '__main__':


def run():
    if os.path.exists(path="paths.geojson"):
        graph = read_to_graph(file_name="paths.geojson", should_densify_segments=True, distance=2)

        db = Database(
            dbname=os.environ.get("PGDATABASE"),
            user=os.environ.get("PGUSER"),
            host=os.environ.get("PGHOST"),
            password=os.environ.get("PGPASSWORD")
        )
        db.connect()
        db.insert_nodes_edges(graph=graph)
        db.insert_shapefile_to_postgis(shapefile_path='data/place/places.shp', table_name='place')
        db.insert_shapefile_to_postgis(shapefile_path='data/building/building.shp', table_name='building')
        db.close()
    else:
        print("❌ File not found!\nExiting...")
