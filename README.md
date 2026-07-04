# ⚡ AI Code Modernization Engine

**Created by Pradeep Kumar Sharma | NIT Kurukshetra**

An enterprise-grade, multi-agent AI pipeline designed to autonomously refactor legacy monolithic codebases into modern, scalable architectures. By leveraging Graph-RAG (Retrieval-Augmented Generation) and Agentic Orchestration, this engine understands complex code relationships and physically rewrites them into modular directory structures.

## 🌟 Key Features

* **Live Graph-RAG Context:** Integrates directly with a local **Neo4j Graph Database** to query the Abstract Syntax Tree (AST) of the legacy codebase, allowing the AI to understand deep file, class, and function dependencies.
* **Multi-Agent Orchestration:** Powered by **CrewAI** and **Groq's Llama-3.3-70B**, featuring three distinct autonomous agents:
  * 🏗️ **The Architect:** Analyzes the database and designs a modern folder structure.
  * 💻 **The Coder:** Drafts robust, functional Python logic for the new architecture.
  * 🛡️ **The QA Engineer:** Reviews the generated code for syntax errors and acts as the gatekeeper.
* **Autonomous File Generation:** Uses custom Python tools to physically create directories and write the modernized `.py` files directly to the local hard drive.
* **Interactive UI:** A clean, responsive web dashboard built with **Streamlit** for seamless pipeline execution and real-time output monitoring.

## 🏗️ Architecture Flow

1. **User Input:** User triggers the pipeline via the Streamlit web interface.
2. **Context Retrieval:** The Architect agent queries the local Neo4j database using a custom Cypher-query tool.
3. **Logic Generation:** The Coder agent processes the blueprint and writes the refactored code.
4. **Validation & Execution:** The QA Engineer reviews the code and triggers the File Writer tool.
5. **Output:** A completely new, modular project tree is generated in the `modernized_output/` directory.

## 🚀 Getting Started

### Prerequisites
* Python 3.10+
* **Neo4j Desktop** (Running locally on default port 7687)
* A valid **Groq API Key**

### Installation

1. Clone the repository:
   ```bash
   git clone [https://github.com/yourusername/code-modernization-engine.git](https://github.com/pradeepsharma-4171/code-modernization-engine.git)
   cd code-modernization-engine
