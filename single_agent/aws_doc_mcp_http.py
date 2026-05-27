import threading, time

from datetime import timedelta

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from mcp.client.streamable_http import streamable_http_client
from mcp.server import FastMCP

from strands import Agent
from strands.tools.mcp import MCPClient
from strands.models import BedrockModel

bedrock_model = BedrockModel(model_id="amazon.nova-micro-v1:0",region_name="us-east-1",)

mcp = FastMCP("Calculator Server")

@mcp.tool(description="Calculate the result of a mathematical expression.")
def calculate(x:int, y: str) -> int:
    """Calculate the result of a mathematical expression."""
    return x+y

@mcp.tool(description="This is a long running tool.")
def long_running_tool(name: str) -> str:
    """Sleep for a specified number of seconds."""
    time.sleep(25)
    return f"Tool completed for {name}"

def start_mcp_server():
    mcp.run(transport="streamable-http", mount_path="mcp")
    
    
thread  = threading.Thread(target=start_mcp_server, daemon=True)
thread.start()

def create_streamable_http_transport():
    return streamable_http_client(
        base_url="http://localhost:8000/mcp",
        session=ClientSession(),
        parameters=StdioServerParameters(),
    )
    
streamable_http_transport = MCPClient(create_streamable_http_transport)