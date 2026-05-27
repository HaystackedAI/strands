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

stdio_mcp_client = MCPClient(
    lambda: stdio_client(
        StdioServerParameters(
            command="uvx", args=["awslabs.aws-documentation-mcp-server@latest"]
        )
    )
)


with stdio_mcp_client: 
    tools = stdio_mcp_client.list_tools_sync()
    
    agent = Agent(model = bedrock_model,tools = tools,)
    response = agent("What is Amazon Bedrock pricing model. Be concise.")
    