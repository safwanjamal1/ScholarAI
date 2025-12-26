from dotenv import load_dotenv # to load environment variables from .env file
from pydantic import BaseModel # to create structured response model
from langchain_openai import ChatOpenAI # LLM wrapper for OpenAI chat models
from langchain_anthropic import ChatAnthropic # LLM wrapper for Anthropic chat models
from langchain_core.prompts import ChatPromptTemplate # to create chat prompts
from langchain_core.output_parsers import PydanticOutputParser # to parse LLM output into pydantic models
from langchain.agents import create_tool_calling_agent # to create an agent that can call tools
from langchain.agents import AgentExecutor # to execute the agent with tools
from tools import search_tool, wiki_tool, save_tool

load_dotenv() # load environment variable file for all required credentials 

class ResearchAgentResponse(BaseModel):
    topic: str # generate a topic based on user query of type string
    summary: str # generate a summary of the research output of type string
    sources: list[str] # list of sources used by agent of type list of strings
    tools_used: list[str] # list of tools used by agent of type list of strings
    

llm = ChatOpenAI(model="gpt-4o-mini")
# llm = ChatOpenAI(model="gpt-4.1-nano")
# llm = ChatAnthropic(model="claude-3-5-sonnet-20241022")

# Tested LLM invocation below:
# response = llm.invoke("Hello, how are you today?")
# print(response)

parser = PydanticOutputParser(pydantic_object=ResearchAgentResponse)

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system", # information to the LLM so it knows what to do
            """
            You are a research assistant that will help generate a research paper.
            Answer the user query and use the neccessary tools. 
            Wrap the output in this format and provide no other text\n{output_format_instructions}
            """,
        ),
        ("placeholder", "{chat_history}"), # chat history between user and agent
        ("human", "{query}"), # from user
        ("placeholder", "{agent_scratchpad}"), # intermediate steps from agent
    ]
).partial(output_format_instructions=parser.get_format_instructions()) # partially fills in the output format instructions    

tools = [search_tool, wiki_tool, save_tool] # list of tools available to the agent
agent = create_tool_calling_agent( 
    llm=llm, # LLM to use
    prompt=prompt, # prompt template to use
    tools=tools # tools available to the agent
)

agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True) # verbose to see intermediate steps of agent
query = input("What can I help you research? ")
raw_response = agent_executor.invoke({"query": query})
# print(raw_response) # printed for debugging


try:
    structured_response = parser.parse(raw_response["output"]) # gets structured text from raw response
    # parser allows us to pick components from the response easily rather than having raw text
    print(structured_response)
except Exception as e:
    print("Error parsing response:", e)
    print("Raw Response -", raw_response)