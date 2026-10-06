import os
from dotenv import load_dotenv, find_dotenv
from langchain.tools import tool
from tavily import TavilyClient


load_dotenv(find_dotenv())
tavily = TavilyClient(api_key=os.getenv("TAV_API_KEY"))

# A tool to search the web for current or recent information
@tool
def web_search(query: str) -> str:
    """Search the web for current or recent information.
       Args:
       query: The search query to send to the web search engine."""

    result = tavily.search(query=query,max_results=5)
    output = []

    for item in result["results"]:
        output.append(
            f"Title: {item['title']}\n"
            f"URL: {item['url']}\n"
            f"Content: {item['content'][:500]}\n"
        )

    return "\n".join(output)