import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.ingestion.ast_parser import analyze_python_file
from src.graph.graph_builder import GraphBuilder
# ... (leave the rest of your code exactly as it is

def scan_and_index_project(project_root: str):
    """
    Crawls the project directory, extracts metadata from Python files,
    and indexes them inside the Neo4j graph database.
    """
    print(f"Starting codebase ingestion for: {project_root}\n")
    
    # Initialize our database builder
    builder = GraphBuilder()
    
    # Folders we explicitly want to skip to avoid parsing noise
    ignored_dirs = {'.git', 'venv', '.venv', '__pycache__', '.pytest_cache', 'egg-info'}

    file_count = 0

    # Walk through all directories and files
    for root, dirs, files in os.walk(project_root):
        # Filter out ignored directories in-place
        dirs[:] = [d for d in dirs if d not in ignored_dirs]
        
        for file in files:
            if file.endswith('.py'):
                full_path = os.path.join(root, file)
                print(f"Parsing: {os.path.relpath(full_path, project_root)}")
                
                try:
                    # 1. Parse structural metrics from the file
                    metadata = analyze_python_file(full_path)
                    
                    # Skip if there was a syntax or read error
                    if "error" in metadata:
                        print(f"Skipping {file} due to error: {metadata['error']}")
                        continue
                        
                    # 2. Push the structural nodes and relationships into Neo4j
                    builder.create_code_nodes(metadata)
                    file_count += 1
                    
                except Exception as e:
                    print(f"Failed to process file {file}: {e}")

    # Close the database session cleanly
    builder.close()
    print(f"\nIngestion Complete! Successfully mapped {file_count} Python files to Neo4j.")

if __name__ == "__main__":
    # Get the absolute path of your current project root directory
    current_project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    
    # Index your own project engine into the graph
    scan_and_index_project(current_project_dir)