"""Debug script to test mem0 configuration directly."""
import os

# Set env vars before any imports
os.environ["MEM0_LLM_MODEL"] = "amazon.nova-pro-v1:0"
os.environ["MEM0_EMBEDDER_MODEL"] = "amazon.titan-embed-text-v2:0"
os.environ["BYPASS_TOOL_CONSENT"] = "true"

print("Step 1: Testing boto3 Bedrock access...")
import boto3

client = boto3.client("bedrock-runtime", region_name="us-east-1")

# Test Nova Pro
try:
    import json
    response = client.invoke_model(
        modelId="amazon.nova-pro-v1:0",
        body=json.dumps({
            "messages": [{"role": "user", "content": [{"text": "Say hello"}]}]
        }),
        contentType="application/json"
    )
    print("  ✅ Nova Pro works!")
except Exception as e:
    print(f"  ❌ Nova Pro error: {e}")

# Test Titan Embed
try:
    response = client.invoke_model(
        modelId="amazon.titan-embed-text-v2:0",
        body=json.dumps({
            "inputText": "test embedding"
        }),
        contentType="application/json"
    )
    print("  ✅ Titan Embed V2 works!")
except Exception as e:
    print(f"  ❌ Titan Embed V2 error: {e}")

print("\nStep 2: Testing mem0 Memory initialization...")
try:
    from mem0 import Memory as Mem0Memory

    config = {
        "embedder": {
            "provider": "aws_bedrock",
            "config": {"model": "amazon.titan-embed-text-v2:0"},
        },
        "llm": {
            "provider": "aws_bedrock",
            "config": {
                "model": "amazon.nova-pro-v1:0",
                "temperature": 0.1,
                "max_tokens": 2000,
            },
        },
        "vector_store": {
            "provider": "faiss",
            "config": {
                "embedding_model_dims": 1024,
                "path": "/tmp/mem0_384_faiss",
            },
        },
    }

    memory = Mem0Memory.from_config(config_dict=config)
    print("  ✅ Memory initialized!")

    print("\nStep 3: Storing a test memory...")
    result = memory.add(
        [{"role": "user", "content": "My name is DD and I love biryani"}],
        user_id="dd_user"
    )
    print(f"  ✅ Stored: {result}")

    print("\nStep 4: Retrieving memories...")
    try:
        memories = memory.get_all(user_id="dd_user")
    except (ValueError, TypeError):
        # Newer mem0ai versions use filters instead
        memories = memory.get_all(filters={"user_id": "dd_user"})
    print(f"  ✅ Retrieved: {memories}")

except Exception as e:
    print(f"  ❌ Error: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()
