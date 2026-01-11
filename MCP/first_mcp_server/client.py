
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.agents import create_agent
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import asyncio, os

load_dotenv()

async def main():
    # Set up MCP client
    client = MultiServerMCPClient(
        {
            "math": {
                "command": "python",
                "args": ["mathsserver.py"],  # Ensure absolute path if needed
                "transport": "stdio",
            },
            "weather": {
                "url": "http://localhost:8000/mcp",  # Ensure server is running
                "transport": "streamable_http",
            }
        }
    )

    os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

    # Get MCP tools
    tools_list = await client.get_tools()
    print("MCP Tools:", tools_list)

    # Map tools by their actual names
    tools_dict = {tool.name.lower(): tool for tool in tools_list}

    # Initialize model
    model = ChatGroq(model="llama-3.1-8b-instant")

    # Create agent with correct tools
    agent = create_agent(
        model,
        tools=[
            tools_dict["add"],         # for addition
            tools_dict["multiple"],    # for multiplication
            tools_dict["get_weather"], # for weather
        ],
        system_prompt=(
            "You are an assistant with access to MCP tools only.\n"
            "For math questions, always use the MCP math tools ('add' or 'multiple').\n"
            "For weather questions, always use the 'get_weather' MCP tool.\n"
            "Do NOT compute math or search the web internally.\n"
        ),
    )

    # Math example
    math_response = await agent.ainvoke(
        {"messages": [{"role": "user", "content": "what's (3 + 5) x 12?"}]}
    )
    print("raka Math response:", math_response['messages'][-1].content)

    # Weather example
    weather_response = await agent.ainvoke(
        {"messages": [{"role": "user", "content": "what is the weather in California?"}]}
    )
    print("Weather response:", weather_response['messages'][-1].content)

asyncio.run(main())
