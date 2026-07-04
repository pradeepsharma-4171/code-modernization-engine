import ast
import os
from typing import Dict, List, Any

class CodebaseVisitor(ast.NodeVisitor):
    """
    Traverses the Abstract Syntax Tree (AST) of a Python file 
    to extract key structural components.
    """
    def __init__(self):
        self.classes: List[str] = []
        self.functions: List[str] = []
        self.imports: List[str] = []

    def visit_ClassDef(self, node: ast.ClassDef):
        """Extracts class names."""
        self.classes.append(node.name)
        # Continue traversing inside the class
        self.generic_visit(node)

    def visit_FunctionDef(self, node: ast.FunctionDef):
        """Extracts function and method names."""
        self.functions.append(node.name)
        self.generic_visit(node)

    def visit_Import(self, node: ast.Import):
        """Extracts standard imports (e.g., import os)."""
        for alias in node.names:
            self.imports.append(alias.name)
        self.generic_visit(node)

    def visit_ImportFrom(self, node: ast.ImportFrom):
        """Extracts specific imports (e.g., from typing import List)."""
        if node.module:
            self.imports.append(node.module)
        self.generic_visit(node)

def analyze_python_file(filepath: str) -> Dict[str, Any]:
    """
    Reads a Python file, parses it into an AST, and returns a 
    structured dictionary of its components.
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Could not find file: {filepath}")

    with open(filepath, 'r', encoding='utf-8') as file:
        file_content = file.read()
    
    try:
        # Parse the raw text into a structural tree
        tree = ast.parse(file_content)
    except SyntaxError as e:
        return {"error": f"Syntax error in {filepath}: {e}"}

    visitor = CodebaseVisitor()
    visitor.visit(tree)
    
    # Return the extracted metadata ready for our Graph Database
    return {
        "file_path": filepath,
        "file_name": os.path.basename(filepath),
        "classes": visitor.classes,
        "functions": visitor.functions,
        "dependencies": visitor.imports
    }

# Quick test execution
if __name__ == "__main__":
    # Test it on itself!
    current_file = os.path.abspath(__file__)
    metadata = analyze_python_file(current_file)
    
    print("Extraction Successful. Data ready for Graph Database:")
    import json
    print(json.dumps(metadata, indent=4))