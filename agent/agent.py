"""Modern MCP agent using LangChain (2026)"""

import asyncio
import json

from langchain_openai import ChatOpenAI
from langchain_core.tools import Tool

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def run_agent():
    """Run a simple MCP-powered agent"""

    server = StdioServerParameters(
        command="python",
        args=["server/mcp_server.py"]
    )

    async with stdio_client(server) as (read, write):
        async with ClientSession(read, write) as session:

            await session.initialize()

            # Discover MCP tools
            mcp_tools = await session.list_tools()
            print("Discovered MCP tools:", mcp_tools)

            # Wrap MCP tools as LangChain Tools
            lc_tools = []

            for tool in mcp_tools:
                # unpack tuple or dict
                tool_name, tool_desc = tool  # if tuple
                # tool_name = tool['name']; tool_desc = tool.get('description')  # if dict

                async def call_tool(input_text: str, tool_name=tool_name):
                    try:
                        args = json.loads(input_text)
                    except json.JSONDecodeError:
                        args = {"query": input_text}
                    return str(await session.call_tool(tool_name, args))

                # wrap in Tool, make sure description is string
                lc_tools.append(
                    Tool(
                        name=tool_name,
                        func=lambda x, f=call_tool: asyncio.run(f(x)),
                        description=str(
                            tool_desc) if tool_desc else f"MCP tool {tool_name}"
                    )
                )

            # LLM
            llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

            # Simple orchestrator
            user_query = "What is the company vacation policy?"

            # Example: pick the first tool (you can improve logic here)
            selected_tool = lc_tools[0]
            print(
                f"Calling tool: {selected_tool.name} with query: {user_query}")
            tool_result = selected_tool.func(json.dumps({"query": user_query}))

            # Use LLM to generate response based on tool output
            response = llm(
                f"Answer this question based on tool output:\nTool Output: {tool_result}\nQuestion: {user_query}")

            print("\nAgent Response:\n", response)


if __name__ == "__main__":
    asyncio.run(run_agent())
