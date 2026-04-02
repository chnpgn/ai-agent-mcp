from mcp.server.fastmcp import FastMCP
from tools import get_users, calculate, search_docs

mcp = FastMCP("AI Agent MCP Server")


@mcp.tool()
def get_users_tool():
    """Fetch users from database"""
    return get_users()


@mcp.tool()
def calculate_tool(a: int, b: int):
    """Add two numbers"""
    return calculate(a, b)


@mcp.tool()
def search_docs_tool(query: str):
    """Search company documentation"""
    return search_docs(query)


if __name__ == "__main__":
    mcp.run()
