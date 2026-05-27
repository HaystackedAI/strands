from strands import Agent
from strands.models import BedrockModel
from strands.tools.mcp import MCPClient
from mcp.client.streamable_http import streamable_http_client

bedrock_model = BedrockModel(model_id="amazon.nova-micro-v1:0",region_name="us-east-1",)
    

def main():
    # Connect to the quiz MCP server
    print("\nConnecting to MCP Server...")
    mcp_quiz_server = MCPClient(lambda: streamable_http_client("http://localhost:8080/mcp"))
    
    # Example of direct tool usage
    # with mcp_quiz_server:
    #     mcp_tools = mcp_quiz_server.list_tools_sync()
    #     agent = Agent(tools=mcp_tools)
        
    #     # Direct tool call via MCP
    #     topics = agent.tool.list_quiz_topics()
    #     print(f"Available topics:\n{topics}")



    try:
        with mcp_quiz_server:

            # Create the subject expert agent with a system prompt
            subject_expert = Agent(
                model=bedrock_model,
                system_prompt="""You are a Computer Science Subject Expert with access to 
                an external quiz service. You can list available quiz topics, retrieve 
                quizzes for students, ask the user to take a quiz, and check their answers.

                When a student requests a quiz:
                1. Show available topics if they ask what's available
                2. Retrieve the specific quiz they want
                3. Present questions clearly, one at a time, with numbered options
                5. After they have provided all answers, check their responses against the
                   correct answers
                6. Once done with the quiz, give encouraging feedback and explanations

                Rules:
                - You must use the tools provided to you by the MCP server.
                - You must NOT make up your own quiz topics or questions.
                - The quiz data includes correct answers, so you can grade responses yourself.
                """
            )

            # List the tools available on the MCP server...
            mcp_tools = mcp_quiz_server.list_tools_sync()
            print(f"Available tools: {[tool.tool_name for tool in mcp_tools]}")

            # ... and add them to the agent
            subject_expert.tool_registry.process_tools(mcp_tools)

            # Start an interactive learning session
            print("\n👨‍💻 CS Subject Expert with MCP Integration")
            print("=" * 50)
            print("\n📋 Try: 'What quiz topics are available?' or 'Give me a Python quiz'")

            while True:
                user_input = input("\n🎯 Your request: ")
                
                if user_input.lower() in ["exit", "quit", "bye"]:
                    print("👋 Happy learning!")
                    break
                
                print("\n🤔 Processing...\n")
                subject_expert(user_input)
               
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        print("💡 Make sure the quiz service is running: python quiz_mcp_server.py")




if __name__ == "__main__":
    main()