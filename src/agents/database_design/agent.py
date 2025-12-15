import os
import sys
from google.adk.agents import LlmAgent
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from utils.file_loader import load_instructions_file

database_agent = LlmAgent(
    name="database_agent",
    model="gemini-2.5-flash",
    instruction=load_instructions_file("agents/database_design/instructions.txt"),
    description=load_instructions_file("agents/database_design/description.txt"),
    output_key="database_agent_output"
)
