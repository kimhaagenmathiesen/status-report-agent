from llama_index.core.agent.workflow import AgentWorkflow
from llama_index.llms.ollama import Ollama
from llama_index.core.agent.workflow import ReActAgent
import asyncio
from llama_index.core.workflow import Context
import pandas as pd


class StatusGenerator:
    def __init__(self):
        """
        Initialize the StatusGenerator with empty components. 
        Actual initialization happens in async_init.
        """
        self.llm = None
        self.agents = None
        self.workflow = None
        self.ctx = None

    async def async_init(self):
        """
        Asynchronously initialize the LLM, agents, workflow, and context.
        """
        self.llm = Ollama(model="gemma3:27b", request_timeout=3000.0)
        self.agents = self.init_agents()
        self.workflow = self.init_workflow()
        self.ctx = Context(self.workflow)

    def init_agents(self):
        """
        Initialize and return the list of agents for the workflow.
        """
        retrieve_agent = ReActAgent(
            name="retrieve_agent",
            description="Returns measurements, dates and comments from a file",
            system_prompt="A helpful assistant that can return data from file.",
            tools=[self.get_data],
            llm=self.llm,
        )
        comments_agent = ReActAgent(
            name="comments_agent",
            description="Returns comments from a given period",
            system_prompt="A helpful assistant that can return comments.",
            tools=[self.get_comments],
            llm=self.llm,
        )
        return [retrieve_agent, comments_agent]

    def init_workflow(self):
        """
        Initialize and return the AgentWorkflow that coordinates agent execution.
        """
        return AgentWorkflow(
            agents=self.agents,
            root_agent="retrieve_agent",
            initial_state={"function_calls": 0},
            state_prompt="Current state: {state}. User message: {msg}",
        )

    async def get_state(self):
        """
        Retrieve the current state from the context.
        """
        return await self.ctx.get("state")

    async def set_state(self, cur_state):
        """
        Set the current state in the context.
        
        Args:
            cur_state (dict): The state to set in the context.
        """
        return await self.ctx.set("state", cur_state)
    
    async def get_data(self, start_date: str, end_date: str, file: str) -> dict:
        """
        Return a pandas DataFrame containing rows from the file within the specified date range.
        
        Args:
            start_date (str): The start date in format "dd-mm-yyyy".
            end_date (str): The end date in format "dd-mm-yyyy".
            file (str): The path to the CSV file.
        
        Returns:
            dict: Filtered DataFrame as a dictionary.
        """
        df = pd.read_csv(file, names=["Dato", "Måling", "Kommentar"], header=None)
        df["Dato"] = pd.to_datetime(df["Dato"], dayfirst=True, errors='coerce')
        start_date = pd.to_datetime(start_date, format="%d-%m-%Y")
        end_date = pd.to_datetime(end_date, format="%d-%m-%Y")
        df = df[(df["Dato"] >= start_date) & (df["Dato"] <= end_date)]
        cur_state = await self.ctx.get("state")
        cur_state["function_calls"] += 1
        await self.ctx.set("state", cur_state)
        return df

    async def get_comments(self, measurements: dict) -> list[str]:
        """
        Return a list of comments from the provided measurements.
        
        Args:
            measurements (dict): The DataFrame or equivalent dict containing comments.
        
        Returns:
            list[str]: A list of comment strings.
        """
        res = list(measurements["Kommentar"])
        cur_state = await self.ctx.get("state")
        cur_state["function_calls"] += 1
        await self.ctx.set("state", cur_state)
        return res

    async def run_agent(self, prompt):
        """
        Run the workflow with the provided user prompt.
        
        Args:
            prompt (str): The user input to process.
        
        Returns:
            The result of the workflow execution.
        """
        print(prompt)
        return await self.workflow.run(user_msg=prompt, ctx=self.ctx)


async def main():
    """
    Main entry point for running the StatusGenerator.
    """
    calc_agent = StatusGenerator()
    await calc_agent.async_init()
    response = await calc_agent.run_agent(
        "Hent data fra perioden 01-01-2025 til 01-02-2025 i input.csv og print data, måling og kommentar."
    )
    print(response)
    state = await calc_agent.get_state()
    print(state["function_calls"])


if __name__ == "__main__":
    asyncio.run(main())
