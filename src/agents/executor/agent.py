# import os
# import sys
# from google.adk.agents import LlmAgent
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
# from utils.file_loader import load_instructions_file

# executor_agent = LlmAgent(
#     name="executor_agent",
#     model="gemini-2.5-flash",
#     instruction=load_instructions_file("agents/executor/instructions.txt"),
#     description=load_instructions_file("agents/executor/description.txt"),
#     output_key="executor_output"
# )

import os
import sys
from google.adk.agents import LlmAgent
from google.adk.tools import load_memory

# Make project root importable
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from utils.file_loader import load_instructions_file

# ---------------------------------------------------------
# Load Executor Instructions & Description
# ---------------------------------------------------------
instruction_text = load_instructions_file("agents/executor/instructions.txt")
description_text = load_instructions_file("agents/executor/description.txt")

# ---------------------------------------------------------
# Executor Agent (SILENT SYSTEM AGENT)
# ---------------------------------------------------------
executor_agent = LlmAgent(
    name="executor_agent",
    model="gemini-2.5-flash",
    instruction=instruction_text,
    description=description_text,
    output_key="executor_output",
    tools=[load_memory]
   
)

# ---------------------------------------------------------
# Execution Wrapper (ONLY user-facing output lives here)
# ---------------------------------------------------------
# ---------------------------------------------------------
# Execution Wrapper - NO USER-FACING OUTPUT HERE
# ---------------------------------------------------------
async def execute_next_step(state, session_service, memory_service):
    """
    The executor agent has already run and populated state['executor_output'].
    This function does NOT generate any user-facing text.
    It just passes through the executor's output for routing.
    """
    # Simply return the executor output for the router to handle
    return state.get("executor_output", {})