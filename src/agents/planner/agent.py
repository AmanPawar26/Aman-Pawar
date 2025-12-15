# import os
# import sys
# from google.adk.agents import LlmAgent
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
# from utils.file_loader import load_instructions_file

# planner_agent = LlmAgent(
#     name="planner_agent",
#     model="gemini-2.5-flash",
#     instruction=load_instructions_file("agents/planner/instructions.txt"),
#     description=load_instructions_file("agents/planner/description.txt"),
#     output_key="planner_output"
# )

# import os
# import sys
# from google.adk.agents import LlmAgent
# from google.adk.tools import load_memory

# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
# from utils.file_loader import load_instructions_file

# # --- Load instructions and description ---
# instruction_text = load_instructions_file("agents/planner/instructions.txt")
# description_text = load_instructions_file("agents/planner/description.txt")

# # --- Instantiate LLM Planner Agent ---
# planner_agent = LlmAgent(
#     name="planner_agent",
#     model="gemini-2.5-flash",
#     instruction=instruction_text,
#     description=description_text,
#     output_key="planner_output",
#     tools=[load_memory]  # Optional: planner can query memory if needed
# )

# # --- Optional helper function to decide next step using memory ---
# async def plan_next_step(state, session_service, memory_service):
#     """
#     Handles greeting, topic selection, and adaptive next step planning.
#     This wraps the LlmAgent with memory-aware logic.
#     """
#     user_id = state['user_id']
#     app_name = "interview_app"
#     session_id = state['session_id']
#     user_answer = state.get('user_answer', "")

#     # 1️⃣ Check if topic is already selected
#     topic_sessions = await memory_service.search_memory(
#         app_name=app_name,
#         user_id=user_id,
#         query="topic_selected"
#     )

#     if not topic_sessions:
#         # First interaction: prompt topic selection
#         return {
#             "next_agent": "topic_selection",
#             "difficulty": None,
#             "twist": None,
#             "reasoning": "User needs to select an interview topic to begin.",
#             "memory_update": "Interview starting. Awaiting candidate's topic selection."
#         }

#     # 2️⃣ Otherwise, load recent performance
#     recent_sessions = await memory_service.search_memory(
#         app_name=app_name,
#         user_id=user_id,
#         query="expert_question"
#     )

#     # Simple adaptive difficulty: increase if last answer correct
#     if recent_sessions and recent_sessions[-1].get('user_answer_correct'):
#         difficulty = "medium"
#     else:
#         difficulty = "easy"

#     # 3️⃣ Determine next expert agent based on topic
#     topic = topic_sessions[-1]['topic_selected'] if topic_sessions else "Database"
#     next_agent = {
#         "database": "database_agent",
#         "api": "api_agent",
#         "cloud": "cloud_agent"
#     }.get(topic.lower(), "database_agent")

#     return {
#         "next_agent": next_agent,
#         "difficulty": difficulty,
#         "twist": None,
#         "reasoning": f"Continuing {topic} interview based on previous answer.",
#         "memory_update": f"Candidate answer evaluated. Next step planned by Planner."
#     }




# ✅ UPDATED: `agents/planner/agent.py`


import os
import sys
from google.adk.agents import LlmAgent
from google.adk.tools import load_memory

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
)

from utils.file_loader import load_instructions_file

# --- Load planner instructions and description ---
instruction_text = load_instructions_file("agents/planner/instructions.txt")
description_text = load_instructions_file("agents/planner/description.txt")

# --- Instantiate Planner Agent ---
planner_agent = LlmAgent(
    name="planner_agent",
    model="gemini-2.5-flash",
    instruction=instruction_text,
    description=description_text,
    output_key="planner_output",
    tools=[load_memory]  # Planner may read memory, not control flow
    
)

# -------------------------------------------------------------------
# NOTE:
# There is INTENTIONALLY NO greeting or topic-selection logic here.
# The planner LLM decides when to emit next_agent = "topic_selection".
# The executor wrapper is the ONLY place that greets the user.
# -------------------------------------------------------------------
