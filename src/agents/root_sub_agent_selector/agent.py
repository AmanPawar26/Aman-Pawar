# import os
# import sys
# from google.adk.agents import LlmAgent

# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
# from utils.file_loader import load_instructions_file

# # Import the sequential pipeline and expert agents
# from agents.planner_executor_pipeline.agent import planner_executor_pipeline
# from agents.api_backend.agent import api_agent
# from agents.database_design.agent import database_agent
# from agents.cloud.agent import cloud_agent
 
# # ---------------------------------------------------------
# # Root Coordinator - Routes to experts after planner/executor
# # ---------------------------------------------------------
# root_agent = LlmAgent(
#     name="root_interview_coordinator",
#     model="gemini-2.5-flash",
#     instruction=load_instructions_file("agents/root_sub_agent_selector/instructions.txt"),
#     description=load_instructions_file("agents/root_sub_agent_selector/description.txt"),
#     sub_agents=[
#         planner_executor_pipeline,  # Sequential: always runs first
#         api_agent,                   # Conditional: only if executor routes here
#         database_agent,              # Conditional: only if executor routes here
#         cloud_agent                  # Conditional: only if executor routes here
#     ]
# )

import os
import sys
from typing import AsyncGenerator
from typing_extensions import override

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from google.adk.agents import BaseAgent
from google.adk.agents.invocation_context import InvocationContext
from google.adk.events import Event
from agents.planner_executor_pipeline.agent import planner_executor_pipeline
from agents.api_backend.agent import api_agent
from agents.database_design.agent import database_agent
from agents.cloud.agent import cloud_agent

class RootInterviewCoordinator(BaseAgent):
    """
    Custom root agent that deterministically orchestrates the interview.
    """

    planner_executor_pipeline: BaseAgent
    database_agent: BaseAgent
    api_agent: BaseAgent
    cloud_agent: BaseAgent

    model_config = {"arbitrary_types_allowed": True}

    def __init__(self):
        super().__init__(
            name="root_interview_coordinator",
            planner_executor_pipeline=planner_executor_pipeline,
            database_agent=database_agent,
            api_agent=api_agent,
            cloud_agent=cloud_agent,
            sub_agents=[
                planner_executor_pipeline,
                database_agent,
                api_agent,
                cloud_agent,
            ],
        )

    @override
    async def _run_async_impl(
        self, ctx: InvocationContext
    ) -> AsyncGenerator[Event, None]:

        # 1️⃣ ALWAYS run planner + executor
        async for event in self.planner_executor_pipeline.run_async(ctx):
            yield event

        # 2️⃣ Safely retrieve executor output
        executor_output = ctx.session.state.get("executor_output", {})
        
        # If executor_output is stored as JSON string, parse it
        if isinstance(executor_output, str):
            try:
                import json
                executor_output = json.loads(executor_output)
            except json.JSONDecodeError:
                executor_output = {}

        # 3️⃣ Topic selection → if action asks for it, return
        if executor_output.get("action") == "request_topic_selection":
            return

        # 4️⃣ Determine next expert agent
        expert = executor_output.get("expert_agent")

        if expert == "database_agent":
            async for event in self.database_agent.run_async(ctx):
                yield event
            return

        if expert == "api_agent":
            async for event in self.api_agent.run_async(ctx):
                yield event
            return

        if expert == "cloud_agent":
            async for event in self.cloud_agent.run_async(ctx):
                yield event
            return

        # 5️⃣ Safety fallback (should never happen)
        return

# Make sure ADK detects this as the root agent
root_agent = RootInterviewCoordinator()
