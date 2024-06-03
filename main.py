from database.db import Database
from utils.utils import read_to_graph
import os

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
#
#     distance_from_query_point, closest_node = graph.query_closest_location(x=-174320.829365919722477,
#                                                                            y=744498.63213670917321,
#                                                                            label="P1")
#     graph.node_to_csv(closest_node)  # Save to CSV for visualization
#
#     distance, shortest_path = dijkstra(graph=graph, initial=closest_node.label,
#                                        end="n1881")  # From Query Location P1 to N-Block(Node 624)
#
#     if shortest_path:
#         graph.nodes_to_csv(paths=shortest_path, file_name="shortest_path_to_Nblock.csv")
#         graph.nodes_to_csv()
#
#         print(f"{distance}m", f"From {shortest_path[0]} To {shortest_path[-1]}")
#
#     else:
#         print("RouteNotPossible")
#
# else:
#     print("File does not exist, Check file path integrity")
