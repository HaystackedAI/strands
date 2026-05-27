import os
import json
import requests
from datetime import date

from strands import Agent
from strands.models.bedrock import BedrockModel
from strands.tools import tool

# --- Memory file path (persists across sessions) ---
MEMORY_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "memory.json")


def _load_memory():
    """Load memory from disk."""
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r") as f:
            return json.load(f)
    return {}


def _save_memory(data):
    """Save memory to disk."""
    with open(MEMORY_FILE, "w") as f:
        json.dump(data, f, indent=2)


# --- Custom Tools ---

@tool
def remember(key: str, value: str) -> str:
    """Store a piece of information in persistent memory.

    Args:
        key: A short label for what to remember (e.g., 'name', 'city', 'food').
        value: The value to remember (e.g., 'DD', 'Tanjore', 'biryani').

    Returns:
        Confirmation that the info was stored.
    """
    memory = _load_memory()
    memory[key] = value
    _save_memory(memory)
    return f"✅ Stored: {key} = {value}"


@tool
def recall(key: str) -> str:
    """Recall a piece of information from persistent memory.

    Args:
        key: The label to look up (e.g., 'name', 'city', 'food'). Use 'all' to get everything.

    Returns:
        The stored value, or all stored memories.
    """
    memory = _load_memory()
    if key.lower() == "all":
        if not memory:
            return "No memories stored yet."
        return "Here's everything I remember:\n" + "\n".join(
            f"  • {k}: {v}" for k, v in memory.items()
        )
    if key in memory:
        return f"{key}: {memory[key]}"
    # Try fuzzy match
    for k, v in memory.items():
        if key.lower() in k.lower() or k.lower() in key.lower():
            return f"{k}: {v}"
    return f"I don't have anything stored for '{key}'."


@tool
def weather(city: str) -> str:
    """Get the current weather for a given city.

    Args:
        city: The name of the city to get weather for.

    Returns:
        A string describing the current weather conditions.
    """
    try:
        response = requests.get(f"https://wttr.in/{city}?format=j1", timeout=10)
        response.raise_for_status()
        data = response.json()
        current = data["current_condition"][0]
        temp_c = current["temp_C"]
        description = current["weatherDesc"][0]["value"]
        humidity = current["humidity"]
        return f"Weather in {city}: {description}, {temp_c}°C, Humidity: {humidity}%"
    except Exception as e:
        return f"Could not fetch weather for {city}: {str(e)}"


@tool
def age_calculator(birth_year: int, birth_month: int, birth_day: int) -> str:
    """Calculate a person's age given their date of birth.

    Args:
        birth_year: The year of birth (e.g., 2000).
        birth_month: The month of birth (1-12).
        birth_day: The day of birth (1-31).

    Returns:
        A string stating the person's age in years.
    """
    try:
        birth_date = date(birth_year, birth_month, birth_day)
        today = date.today()
        age = today.year - birth_date.year - (
            (today.month, today.day) < (birth_date.month, birth_date.day)
        )
        return f"{age} years old"
    except Exception as e:
        return f"Could not calculate age: {str(e)}"


@tool
def calculator(expression: str) -> str:
    """Evaluate a mathematical expression safely.

    Args:
        expression: A math expression to evaluate (e.g., '365 * 24', '2**10', '100/3').

    Returns:
        The result of the calculation as a string.
    """
    try:
        allowed_chars = set("0123456789+-*/.() ")
        if not all(c in allowed_chars for c in expression):
            return f"Invalid expression: {expression}"
        result = eval(expression)
        return f"{expression} = {result}"
    except Exception as e:
        return f"Could not calculate: {str(e)}"


@tool
def fun_fact(topic: str) -> str:
    """Generate a fun fact about a given topic.

    Args:
        topic: The topic to get a fun fact about.

    Returns:
        A fun fact string.
    """
    facts = {
        "python": "🐍 Python was named after Monty Python, not the snake!",
        "aws": "☁️ AWS has more than 200 services and operates in 33 regions worldwide!",
        "space": "🚀 A day on Venus is longer than a year on Venus!",
        "math": "🔢 111,111,111 × 111,111,111 = 12,345,678,987,654,321!",
        "india": "🇮🇳 India has the world's largest postal network with over 155,000 post offices!",
        "tanjore": "🏛️ The Brihadeeswarar Temple in Tanjore is over 1000 years old and its shadow never falls on the ground at noon!",
        "biryani": "🍚 Hyderabadi Biryani uses the 'Dum' cooking method where rice and meat are slow-cooked together in a sealed pot!",
    }
    topic_lower = topic.lower()
    for key, fact in facts.items():
        if key in topic_lower:
            return fact
    return f"🤔 Here's a general fact: The word '{topic}' has {len(topic)} letters!"


# --- Streaming Callback ---

def streaming_callback(**kwargs):
    """Handle streaming events — print text chunks and tool usage in real time."""
    if "data" in kwargs:
        print(kwargs["data"], end="", flush=True)
    if "current_tool_use" in kwargs and kwargs["current_tool_use"].get("name"):
        tool_name = kwargs["current_tool_use"]["name"]
        print(f"\n🔧 Using tool: {tool_name}", flush=True)


# --- Configure Model ---

model = BedrockModel(
    model_id="amazon.nova-pro-v1:0",
    region_name="us-east-1"
)

# --- Create the Full Agent ---

agent = Agent(
    model=model,
    system_prompt="""You are a fun, helpful AI assistant named Buddy 🤖 with tools and memory!

Your capabilities:
- 🧮 calculator: Evaluate math expressions
- 🌤️ weather: Get real-time weather for any city
- 🎂 age_calculator: Calculate age from birth date
- 🧠 remember: Store user info (key + value) to persistent memory
- 🔍 recall: Retrieve stored info (use key='all' to list everything)
- 🎲 fun_fact: Share fun facts about topics

Rules:
- When the user shares personal info (name, city, food, etc.), use the 'remember' tool to store it
- When the user asks about something they told you before, use the 'recall' tool
- Use emojis and be friendly!
- Be concise but helpful.""",
    tools=[calculator, weather, age_calculator, remember, recall, fun_fact],
    callback_handler=streaming_callback
)

# --- Interactive Chat Loop ---

print("=" * 60)
print("🤖 Buddy — Your Full-Featured AI Agent")
print("   Tools: calculator, weather, age_calculator, memory, fun_fact")
print("   Type 'quit' or 'exit' to end the conversation")
print("=" * 60)

while True:
    try:
        user_input = input("\n🧑 You: ").strip()
        if not user_input:
            continue
        if user_input.lower() in ("quit", "exit", "q"):
            print("\n👋 Goodbye! Your memories are saved for next time.")
            break

        print("\n🤖 Buddy: ", end="", flush=True)
        response = agent(user_input)
        print()  # newline after streaming completes

    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
        break
    except Exception as e:
        print(f"\n❌ Error: {e}")
