import os
import sys
from google.adk.agents import SequentialAgent

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

# Import planner and executor
from agents.planner.agent import planner_agent
from agents.executor.agent import executor_agent

# Sequential pipeline: Planner → Executor (always run in order)
planner_executor_pipeline = SequentialAgent(
    name="planner_executor_pipeline",
    sub_agents=[
        planner_agent,
        executor_agent
    ],
    description="Runs Marcus (Planner) then Sofia (Executor) sequentially to prepare context for expert routing."
    
)