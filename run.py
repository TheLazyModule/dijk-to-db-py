import os

from dotenv import load_dotenv

from database.db import Database
from dijkstra.dijkstra import bidirectional_dijkstra
from utils.utils import read_to_graph


def config_env():
    env_mode = os.getenv('ENV', 'production')  # Default to 'production' if ENV mode is not set

    if env_mode == 'development':
        dotenv_file = '.env.development'
    else:
        dotenv_file = '.env.prod'

    load_dotenv(dotenv_file)


def init_db(graph):
    db = Database(
        dbname=os.environ.get("PGDATABASE"),
        user=os.environ.get("PGUSER"),
        host=os.environ.get("PGHOST"),
        password=os.environ.get("PGPASSWORD"),
        sslmode='require'
    )
    db.connect()
    db.insert_nodes_edges(graph=graph)
    db.insert_shapefile_to_postgis(shapefile_path='data/cities/london_cities.shp', table_name='city')


def run():
    config_env()
    if os.path.exists(path="tlrn_test.geojson"):
        graph = read_to_graph(file_name="tlrn_pseudo_mercator_.geojson", should_densify_segments=False, distance=2)
        distance, shortest_path = bidirectional_dijkstra(graph, 'n1', 'n5000')
        print("shortest path:", distance)
        print("path:", shortest_path)
        # init_db(graph=graph)
        # print(len( graph.nodes ))
        # graph.nodes_to_csv('data/london_nodes.csv')

    else:
        print("❌ File not found!\nExiting...")
