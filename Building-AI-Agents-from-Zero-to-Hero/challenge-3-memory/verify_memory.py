import os
from strands import Agent
from strands.models.bedrock import BedrockModel
from strands_tools import mem0_memory

# --- Same env vars as starter.py ---
os.environ["MEM0_LLM_MODEL"] = "amazon.nova-pro-v1:0"
os.environ["MEM0_EMBEDDER_MODEL"] = "amazon.titan-embed-text-v2:0"
os.environ["BYPASS_TOOL_CONSENT"] = "true"

# Configure Amazon Nova Pro via Bedrock
model = BedrockModel(
    model_id="amazon.nova-pro-v1:0",
    region_name="us-east-1"
)

# Same user ID as starter.py
USER_ID = "dd_user"

# Create the agent with persistent memory
agent = Agent(
    model=model,
    system_prompt=f"""You are a helpful AI assistant with persistent memory.
The current user's ID is: {USER_ID}
When retrieving memories, always use user_id="{USER_ID}".""",
    tools=[mem0_memory]
)

# Test persistence — this is a fresh program run!
print("=" * 50)
print("🔄 This is a NEW program run (no conversation history)")
print("=" * 50)
print("\nYou: What do you know about me?")
response = agent(f"List all memories for user_id='{USER_ID}' and tell me everything you know about me.")
print(f"\nAgent: {response}")
