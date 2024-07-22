import os
import timeit

from dotenv import load_dotenv

from database.db import Database
from dijkstra.dijkstra import bidirectional_dijkstra, dijkstra
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
    if os.path.exists(path="tlrn_roehampton.geojson"):
        graph = read_to_graph(file_name="tlrn_roehampton.geojson", should_densify_segments=True, distance=2)
        # print(graph.edges)
        # distance, shortest_path = bidirectional_dijkstra(graph, 'n1', 'n20')
        # Time the execution of the dijkstra algorithm
        # print("Time taken to find shortest path:", timeit.timeit(lambda: dijkstra(graph, 'n1', 'n20'), number=1))
        # print("shortest path:", distance)
        # print("path:", shortest_path)
        init_db(graph=graph)
        # print(len( graph.nodes ))
        graph.nodes_to_csv()

    else:
        print("❌ File not found!\nExiting...")
