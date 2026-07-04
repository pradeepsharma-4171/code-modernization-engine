import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
# ... (leave the rest of your code exactly as it is)
from src.graph.db_connection import Neo4jConnection

class GraphBuilder:
    def __init__(self):
        self.db = Neo4jConnection()

    def close(self):
        self.db.close()

    def create_code_nodes(self, file_data: dict):
        """
        Takes the parsed AST metadata dictionary and writes it into Neo4j using Cypher queries.
        """
        if not self.db.driver:
            print("Database driver not initialized.")
            return

        with self.db.driver.session() as session:
            # 1. Create the base File Node
            file_query = """
            MERGE (f:File {path: $file_path})
            SET f.name = $file_name
            RETURN f
            """
            session.run(file_query, file_path=file_data["file_path"], file_name=file_data["file_name"])

            # 2. Create Class Nodes and link them to the File
            for class_name in file_data["classes"]:
                class_query = """
                MATCH (f:File {path: $file_path})
                MERGE (c:Class {name: $class_name})
                MERGE (f)-[:CONTAINS]->(c)
                """
                session.run(class_query, file_path=file_data["file_path"], class_name=class_name)

            # 3. Create Function Nodes and link them to the File
            for func_name in file_data["functions"]:
                func_query = """
                MATCH (f:File {path: $file_path})
                MERGE (fn:Function {name: $func_name})
                MERGE (f)-[:DEFINES]->(fn)
                """
                session.run(func_query, file_path=file_data["file_path"], func_name=func_name)

            # 4. Create Dependency/Import Nodes
            for dep in file_data["dependencies"]:
                dep_query = """
                MATCH (f:File {path: $file_path})
                MERGE (d:Module {name: $dep_name})
                MERGE (f)-[:DEPENDS_ON]->(d)
                """
                session.run(dep_query, file_path=file_data["file_path"], dep_name=dep)
                
        print(f"Successfully mapped structural nodes for {file_data['file_name']} into the graph!")

# Quick Test to verify it writes properly
if __name__ == "__main__":
    from src.ingestion.ast_parser import analyze_python_file
    import os

    # Let's parse the parser script itself as sample data
    sample_file = os.path.abspath("src/ingestion/ast_parser.py")
    parsed_data = analyze_python_file(sample_file)

    # Push it to Neo4j
    builder = GraphBuilder()
    builder.create_code_nodes(parsed_data)
    builder.close()