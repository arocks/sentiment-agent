import asyncio
import logging
import os
import json

import httpx
from fastmcp import FastMCP

logger = logging.getLogger(__name__)
logging.basicConfig(format="[%(levelname)s]: %(message)s", level=logging.INFO)

mcp = FastMCP("Hacker News Search MCP Server")


@mcp.tool()
def get_top_hn_results(
    search_term: str = "Cloud Run"
):
    """Get top stories from Hacker News

    Args:
        search_term: String to search for (e.g. "Cloud Run")


    Returns:
        A dictionary containing the top stories, or an error message if the request fails.
    """
    logger.info(
        f"--- 🛠️ Tool: get_top_hn_results called for searching {search_term} ---"
    )
    try:
        response = httpx.get(
            #"https://hn.algolia.com/api/v1/search_by_date?query=%22cloud%20run%22&tags=comment"
            f"https://hn.algolia.com/api/v1/search_by_date",
            params={"query": '"' + search_term + '"', "tags": "comment"},
        )
        response.raise_for_status()

        data = response.json()
        if "hits" not in data:
            logger.error(f"❌ hits not found in response: {data}")
            return {"error": "Invalid API response format."}
        logger.info(f"✅ API response: {data}")
        hits = data["hits"]
        comments = [hit.get("comment_text","") for hit in hits]
        result = {"comments": comments }
        return result
    except httpx.HTTPError as e:
        logger.error(f"❌ API request failed: {e}")
        return {"error": f"API request failed: {e}"}
    except ValueError:
        logger.error("❌ Invalid JSON response from API")
        return {"error": "Invalid JSON response from API."}

if __name__ == "__main__":
    logger.info(f"🚀 MCP server started on port {os.getenv('PORT', 8080)}")
    # Could also use 'sse' transport, host="0.0.0.0" required for Cloud Run.
    asyncio.run(
        mcp.run_async(
            transport="streamable-http",
            host="0.0.0.0",
            port=os.getenv("PORT", 8080),
        )
    )
