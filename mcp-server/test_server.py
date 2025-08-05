import asyncio

from fastmcp import Client


async def test_server():
    # Test the MCP server using streamable-http transport.
    # Use "/sse" endpoint if using sse transport.
    async with Client("http://localhost:8080/mcp") as client:
        # List available tools
        tools = await client.list_tools()
        for tool in tools:
            print(f"--- 🛠️  Tool found: {tool.name} ---")
        # Call get_top_hn_results tool
        print("--- 🪛  Calling get_top_hn_results tool for Google Cloud ---")
        result = await client.call_tool(
            "get_top_hn_results", {"search_term": "Google Cloud"}
        )
        print(f"--- ✅  Success: {result[0].text} ---")


if __name__ == "__main__":
    asyncio.run(test_server())
