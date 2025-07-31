import logging
import os

from dotenv import load_dotenv
from google.adk.agents import LlmAgent
from google.adk.tools.mcp_tool import MCPToolset, StreamableHTTPConnectionParams

logger = logging.getLogger(__name__)
logging.basicConfig(format="[%(levelname)s]: %(message)s", level=logging.INFO)

load_dotenv()

SYSTEM_INSTRUCTION = (
    "You are a specialized assistant for searching latest comments about a search term from Hacker News and evaluating its overall sentiment. "
    "Your sole purpose is to use the 'get_top_hn_results' tool to answer questions about latest comments. "
    "Then analyse the comments and assign an overall sentiment score from 1 (least favourable) to 10 (most favourable) and explain why you arrived at that score."
    "If the user asks about anything other than latest comments about a search term and its sentiment analysis, "
    "politely state that you cannot help with that topic and can only assist with sentiment-related queries. "
    "Do not attempt to answer unrelated questions or use tools for other purposes."
)


def create_agent() -> LlmAgent:
    """Constructs the ADK sentiment agent."""
    logger.info("--- 🔧 Loading MCP tools from MCP Server... ---")
    logger.info("--- 🤖 Creating ADK Sentiment Search Agent... ---")
    return LlmAgent(
        model="gemini-2.5-flash",
        name="comment_search_agent",
        description="An agent that can help with sentiment analysis by searching the latest comments",
        instruction=SYSTEM_INSTRUCTION,
        tools=[
            MCPToolset(
                connection_params=StreamableHTTPConnectionParams(
                    url=os.getenv("MCP_SERVER_URL", "http://localhost:8080/mcp")
                )
            )
        ],
    )


root_agent = create_agent()
