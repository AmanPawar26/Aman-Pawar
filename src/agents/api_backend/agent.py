import os
import sys
from google.adk.agents import LlmAgent
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from utils.file_loader import load_instructions_file

api_agent = LlmAgent(
    name="api_agent",
    model="gemini-2.5-flash",
    instruction=load_instructions_file("agents/api-backend/instructions.txt"),
    description=load_instructions_file("agents/api-backend/description.txt"),
    output_key="api_agent_output"
)
