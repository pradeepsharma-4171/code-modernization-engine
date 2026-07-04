import os
from dotenv import load_dotenv, find_dotenv
from neo4j import GraphDatabase

# Automatically search up the folder tree to find the .env file
load_dotenv(find_dotenv())

class Neo4jConnection:
    def __init__(self):
        # Pulling your specific credentials from the .env file
        # We set your specific URI and username as fallbacks just to be safe
        uri = os.getenv("NEO4J_URI", "neo4j://127.0.0.1:7687")
        user = os.getenv("NEO4J_USERNAME", "neo4j")
        password = os.getenv("NEO4J_PASSWORD")

        # Security check
        if not password:
            raise ValueError("NEO4J_PASSWORD was not found. Make sure your .env file is saved.")

        # Establish the connection to the graph database
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        """Safely close the database connection."""
        if self.driver:
            self.driver.close()

    def verify_connectivity(self):
        """A quick helper method to test if the connection is working."""
        try:
            self.driver.verify_connectivity()
            return True
        except Exception as e:
            print(f"Connection failed: {e}")
            return False