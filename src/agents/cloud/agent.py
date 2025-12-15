import os
import sys
from google.adk.agents import LlmAgent
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from utils.file_loader import load_instructions_file

cloud_agent = LlmAgent(
    name="cloud_agent",
    model="gemini-2.5-flash",
    instruction=load_instructions_file("agents/cloud/instructions.txt"),
    description=load_instructions_file("agents/cloud/description.txt"),
    output_key="cloud_agent_output"
)
