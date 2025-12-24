from langchain_community.tools import WikipediaQueryRun # tool for searching wikipedia articles
from langchain_community.tools import DuckDuckGoSearchRun # tool for searching the web
from langchain_community.utilities import WikipediaAPIWrapper # wrapper for wikipedia api
from langchain.tools import Tool # tool class to create custom tools
from datetime import datetime # to get current timestamp

# our own python function to save data to text file
def save_to_txt(data: str, filename: str = "research_output.txt"): # need to specify data type for function calling
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted_text = f"--- Research Output ---\nTimestamp: {timestamp}\n\n{data}\n\n"

    with open(filename, "a", encoding="utf-8") as f:
        f.write(formatted_text)
    
    return f"Data successfully saved to {filename}"

save_tool = Tool(
    name="save_text_to_file", # tool name cannot have any spaces
    func=save_to_txt, # function to call when this tool is used
    description="Saves structured research data to a text file.", # description of tool
)

search = DuckDuckGoSearchRun() # tool for web search
search_tool = Tool(
    name="search", # tool name cannot have any spaces
    func=search.run, # function to call when this tool is used
    description="Search the web for information", # description of tool
)

api_wrapper = WikipediaAPIWrapper(top_k_results=1, doc_content_chars_max=150) # return top 1 result with max 100 characters
wiki_tool = WikipediaQueryRun(api_wrapper=api_wrapper) # no need to wrap it in a custom tool as it is already a tool