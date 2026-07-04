import os
import sys
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process, LLM

# --------------------------------------------------
# CREWAI BUG FIX (Neutralize caching leak)
# --------------------------------------------------
import crewai.llms.cache as _crewai_cache
_crewai_cache.mark_cache_breakpoint = lambda msg: msg

# Permanently fix the import path (This MUST happen first!)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

# Import our custom tools
from src.tools.neo4j_tool import query_codebase_architecture
from src.tools.file_writer_tool import write_file

# Load the environment variables
load_dotenv()

# ==========================================
# GROQ PIVOT
# ==========================================
groq_llm = LLM(
    model="groq/llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY")
)

def run_crew():
    """Initializes the ultimate AI pipeline and assigns tasks."""
    
    # --------------------------------------------------
    # AGENT 1: The Architect
    # --------------------------------------------------
    architect = Agent(
        role='Senior Systems Architect',
        goal='Analyze legacy code logic and design highly modular architectures.',
        backstory='You are an elite software architect. You specialize in breaking down monolithic code into modern design patterns.',
        verbose=True,
        allow_delegation=False,
        llm=groq_llm,
        tools=[query_codebase_architecture]
    )

    # --------------------------------------------------
    # AGENT 2: The Coder (Upgraded)
    # --------------------------------------------------
    coder = Agent(
        role="Senior Python Developer",
        goal="Draft robust, functional Python code based on the Architect's blueprint.",
        backstory="You write clean, idiomatic code adhering to PEP 8 standards. You do not use 'pass' statements; you attempt to write the actual logic for database connections, parsers, and pipelines.",
        verbose=True,
        allow_delegation=False,
        llm=groq_llm
        # Notice: The Coder no longer has the file writer tool. They only draft the code.
    )

    # --------------------------------------------------
    # AGENT 3: The QA Engineer (NEW)
    # --------------------------------------------------
    qa_engineer = Agent(
        role="Senior Quality Assurance Engineer",
        goal="Review the Coder's drafted code for bugs, missing imports, and syntax errors, then save the finalized code to disk.",
        backstory="You are a meticulous code reviewer. You ensure all code is production-ready before it gets deployed.",
        verbose=True,
        allow_delegation=False,
        llm=groq_llm,
        tools=[write_file] # The QA Engineer holds the keys to the hard drive.
    )

    # --------------------------------------------------
    # TASK 1: Analysis
    # --------------------------------------------------
    analyze_task = Task(
        description=(
            "Use the 'Neo4j Architecture Query Tool' to extract the live architecture of our codebase. "
            "Identify 3 major structural problems and suggest a modern folder structure to fix it."
        ),
        expected_output='A professional architectural review with a suggested folder tree.',
        agent=architect
    )

    # --------------------------------------------------
    # TASK 2: Logic Generation
    # --------------------------------------------------
    codegen_task = Task(
        description=(
            "Based on the Architect's report, write the actual functional Python code for the newly proposed files. "
            "Do not use simple boilerplate or 'pass' statements. Write the real logic for database connections and data ingestion."
        ),
        expected_output="Raw Python code blocks for each proposed file.",
        agent=coder
    )

    # --------------------------------------------------
    # TASK 3: Review and Save
    # --------------------------------------------------
    qa_task = Task(
        description=(
            "Review the raw code blocks provided by the Coder. Fix any missing imports, bad variable names, or syntax errors. "
            "CRITICAL INSTRUCTION: You MUST use the 'File Writer Tool' to save every single finalized file. "
            "Pass the desired relative path (e.g., 'src/database.py') and the fixed code block to the tool."
        ),
        expected_output="Confirmation that all error-free files have been successfully written to the disk.",
        agent=qa_engineer
    )

    # --------------------------------------------------
    # ORCHESTRATION: The Final Crew
    # --------------------------------------------------
    modernization_crew = Crew(
        agents=[architect, coder, qa_engineer],
        tasks=[analyze_task, codegen_task, qa_task],
        process=Process.sequential,
        verbose=True
    )
    
    result = modernization_crew.kickoff()
    return result

if __name__ == "__main__":
    run_crew()