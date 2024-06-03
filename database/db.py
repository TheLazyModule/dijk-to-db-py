from sqlalchemy import text, create_engine
from sqlalchemy.exc import SQLAlchemyError
import geopandas as gpd

import psycopg2

from utils.utils import extract_node_id

QUERIES = {
    'node': """
        INSERT INTO node (name, geom)
        VALUES (%s, ST_GeomFromText(%s))
        """,

    'edge': """
        INSERT INTO edge (from_node_id, to_node_id,  weight)
        VALUES (%s, %s, %s)
        """
}


class Database:
    def __init__(self, dbname, user, host, password):
        self.dbname = dbname
        self.user = user
        self.host = host
        self.password = password
        self.connection = None

    def connect(self):
        try:
            self.connection = psycopg2.connect(dbname=self.dbname, user=self.user, password=self.password,
                                               host=self.host)
            return True
        except psycopg2.Error as e:
            print(f"❌ Error connecting to the database: {e}")
            return False

    def close(self):
        if self.connection:
            self.connection.close()

    def execute_query(self, query, params=None, fetch=False):
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, params)
            if fetch:
                return cursor.fetchall()
            else:
                self.connection.commit()
            cursor.close()
        except psycopg2.Error as e:
            print(f"❌ Error executing query: {e}")
            self.connection.rollback()

    def insert_nodes_edges(self, graph):
        print("Inserting nodes...")
        for i, node in enumerate(graph.nodes, start=1):
            x, y, label = graph.nodes[node].x, graph.nodes[node].y, graph.nodes[node].label
            point = f'POINT({x} {y})'

            try:
                self.execute_query(
                    QUERIES['node'],
                    (label, point)
                )
                print(f"✅ Inserted node {i}")
            except:
                print("❌ Unexpected Error occurred when inserting nodes, exiting...")
                return
            else:
                print("✅ Inserted 'nodes' successfully")

            print("Inserting edges...")
            try:
                for i, edge in enumerate(graph.weights, start=1):
                    self.execute_query(
                        QUERIES['edge'],
                        (
                            extract_node_id(edge[0]),
                            extract_node_id(edge[1]),
                            graph.weights[edge]
                        )
                    )
                    print(f"✅ Inserted edge {i}")
            except:
                print("❌ Unexpected Error occurred when inserting edges, exiting...")
                return
            else:
                print("✅ Inserted 'nodes' successfully")

        print("✅ Insertion completed successfully without any errors..")

    def insert_shapefile_to_postgis(self, shapefile_path, table_name):
        if not self.connection:
            print("✅ Database connection is not established.")
            return

        # Read the shapefile
        try:
            gdf = gpd.read_file(shapefile_path)
            print("✅ Shapefile read successfully.")
        except Exception as e:
            print(f"❌ Error reading shapefile: {e}")
            return

        # Create SQLAlchemy engine
        try:
            engine = create_engine(f'postgresql+psycopg2://{self.user}:{self.password}@{self.host}/{self.dbname}')
            print("✅ SQLAlchemy engine created.")
        except SQLAlchemyError as e:
            print(f"❌ Error creating SQLAlchemy engine: {e}")
            return

        # Check the connection using SQLAlchemy
        try:
            with engine.connect() as connection:
                connection.execute(text("SELECT 1"))
            print("✅ SQLAlchemy engine connection established.")
        except SQLAlchemyError as e:
            print(f"❌ Error connecting with SQLAlchemy engine: {e}")
            return

        # Prepare data for insertion
        gdf = gdf[['name', 'geometry']]
        gdf = gdf.rename(columns={'geometry': 'geom'})
        gdf = gdf.set_geometry('geom')

        # Insert data into PostGIS
        try:
            gdf.to_postgis(table_name, engine, if_exists='append', index=False)
            print(f"✅ Data inserted into table '{table_name}' successfully.")
        except Exception as e:
            print(f"❌ Error inserting data into PostGIS: {e}")
            return
