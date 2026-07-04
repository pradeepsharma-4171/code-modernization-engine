import os
import sys
from crewai.tools import tool

# Permanently fix the import path for the tool
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.graph.db_connection import Neo4jConnection

@tool("Neo4j Architecture Query Tool")
def query_codebase_architecture(search_query: str) -> str:
    """
    Queries the local Neo4j graph database to retrieve the overall architecture 
    of the project, including files, classes, functions, and their dependencies.
    ALWAYS pass "all" as the search_query.
    """
    db = Neo4jConnection()
    if not db.driver:
        return "Error: Could not connect to Neo4j Database. Is Neo4j Desktop running?"
    
    # A Cypher query to pull the exact blueprint we created earlier
    query = """
    MATCH (f:File)
    OPTIONAL MATCH (f)-[:CONTAINS]->(c:Class)
    OPTIONAL MATCH (f)-[:DEFINES]->(fn:Function)
    OPTIONAL MATCH (f)-[:DEPENDS_ON]->(d:Module)
    RETURN f.name AS file, 
           collect(DISTINCT c.name) AS classes, 
           collect(DISTINCT fn.name) AS functions,
           collect(DISTINCT d.name) AS dependencies
    """
    
    result_string = "LIVE CODEBASE ARCHITECTURE FROM DATABASE:\n\n"
    
    try:
        with db.driver.session() as session:
            results = session.run(query)
            for record in results:
                result_string += f"File: {record['file']}\n"
                result_string += f" - Classes: {', '.join(record['classes']) or 'None'}\n"
                result_string += f" - Functions: {', '.join(record['functions']) or 'None'}\n"
                result_string += f" - Dependencies: {', '.join(record['dependencies']) or 'None'}\n\n"
        db.close()
        return result_string
    except Exception as e:
        db.close()
        return f"Database Query Failed: {e}"