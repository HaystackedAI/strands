import os
from strands import Agent
from strands.models.bedrock import BedrockModel
from strands_tools import mem0_memory

# --- Configure mem0 to use Nova Pro as its internal LLM ---
# Without this, mem0 defaults to Claude Haiku which may not be enabled
os.environ["MEM0_LLM_MODEL"] = "amazon.nova-pro-v1:0"
os.environ["MEM0_EMBEDDER_MODEL"] = "amazon.titan-embed-text-v2:0"
os.environ["BYPASS_TOOL_CONSENT"] = "true"

# Configure Amazon Nova Pro via Bedrock
model = BedrockModel(
    model_id="amazon.nova-pro-v1:0",
    region_name="us-east-1"
)

# User ID — must be the same in verify_memory.py for persistence to work
USER_ID = "dd_user"

# Create the agent with persistent memory (FAISS-backed)
agent = Agent(
    model=model,
    system_prompt=f"""You are a helpful AI assistant with persistent memory.
The current user's ID is: {USER_ID}
When storing or retrieving memories, always use user_id="{USER_ID}".
When the user shares personal info, store it. When they ask, retrieve it.""",
    tools=[mem0_memory]
)

# --- Store memories directly using tool calls ---

print("=" * 50)
print("Storing memories...")

# Store facts directly
agent.tool.mem0_memory(
    action="store",
    content="My name is DD and I love biryani",
    user_id=USER_ID
)
print("✅ Stored: name is DD, loves biryani")

agent.tool.mem0_memory(
    action="store",
    content="I live in Tanjore and my favorite color is blue",
    user_id=USER_ID
)
print("✅ Stored: lives in Tanjore, favorite color blue")

agent.tool.mem0_memory(
    action="store",
    content="I work as a cloud engineer and I enjoy hiking on weekends",
    user_id=USER_ID
)
print("✅ Stored: cloud engineer, enjoys hiking")

# --- Now ask the agent to recall ---

print("\n" + "=" * 50)
print("You: What do you know about me?")
response = agent(f"Retrieve all memories for user_id='{USER_ID}' and tell me what you know about me.")
print(f"Agent: {response}")

print("\n" + "=" * 50)
print("✅ Memory stored on disk! Now run 'python verify_memory.py' to verify persistence.")
