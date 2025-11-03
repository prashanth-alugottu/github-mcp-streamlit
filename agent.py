import asyncio
from dotenv import load_dotenv
load_dotenv()

import os
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent


GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
DESKTOP_PATH = os.getenv("DESKTOP_PATH", r"C:\Users\Prashanth\Desktop")

async def run_agent_async(user_query: str) -> str:
    """
    Run the MCP agent with the given user query asynchronously.
    
    Args:
        user_query: The user's request/question
        
    Returns:
        The agent's response as a string
    """
    
    # Initialize MCP Client with GitHub and Filesystem servers
    client = MultiServerMCPClient(
        {
            "github": {
                "command": "npx",
                "args": [
                    "-y",
                    "@modelcontextprotocol/server-github"
                ],
                "env": {
                    "GITHUB_PERSONAL_ACCESS_TOKEN": GITHUB_TOKEN
                },
                "transport": "stdio"
            },
            "filesystem": {
                "command": "npx",
                "args": [
                    "-y",
                    "@modelcontextprotocol/server-filesystem",
                    DESKTOP_PATH
                ],
                "transport": "stdio"
            }
        }
    )
    
    try:
        # Get available tools from MCP servers
        tools = await client.get_tools()
        
        # Initialize the LLM
        llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0.7,
            max_tokens=2000
        )
        
        # Create the agent
        agent = create_agent(
            model=llm,
            tools=tools,
            system_prompt=(
                "You are a helpful AI assistant with access to GitHub and Filesystem tools. "
                "You can help users manage files, create repositories, and perform various tasks. "
                "Always provide clear explanations of what you're doing and the results."
            )
        )
        
        # Invoke the agent with the user query
        response =await agent.ainvoke({
            "messages": [{"role": "user", "content": user_query}]
        })
        
        # Extract the response content
        agent_response = response['messages'][-1].content
        
        return agent_response
    
    except Exception as e:
        return f"Error executing agent: {str(e)}"


def run_agent_sync(user_query: str) -> str:
    """
    Synchronous wrapper for the async agent function.
    Use this if you need synchronous execution.
    """
    return asyncio.run(run_agent_async(user_query))
