import requests
from datetime import datetime, date
from strands import Agent
from strands.models.bedrock import BedrockModel
from strands.tools import tool

# Configure Amazon Nova Pro via Bedrock
model = BedrockModel(
    model_id="amazon.nova-pro-v1:0",
    region_name="us-east-1"
)

# --- Custom Tools ---
# skill sprint\challenge-2-tools"
# python starter.py
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
        return f"Age: {age} years old"
    except Exception as e:
        return f"Could not calculate age: {str(e)}"


@tool
def unit_converter(value: float, from_unit: str, to_unit: str) -> str:
    """Convert a value from one unit to another. Supports km/miles, kg/lbs, C/F, cm/inches.

    Args:
        value: The numeric value to convert.
        from_unit: The source unit (km, miles, kg, lbs, celsius, fahrenheit, cm, inches).
        to_unit: The target unit (km, miles, kg, lbs, celsius, fahrenheit, cm, inches).

    Returns:
        A string with the converted value.
    """
    conversions = {
        ("km", "miles"): lambda v: v * 0.621371,
        ("miles", "km"): lambda v: v * 1.60934,
        ("kg", "lbs"): lambda v: v * 2.20462,
        ("lbs", "kg"): lambda v: v * 0.453592,
        ("celsius", "fahrenheit"): lambda v: (v * 9 / 5) + 32,
        ("fahrenheit", "celsius"): lambda v: (v - 32) * 5 / 9,
        ("cm", "inches"): lambda v: v * 0.393701,
        ("inches", "cm"): lambda v: v * 2.54,
    }

    key = (from_unit.lower(), to_unit.lower())
    if key in conversions:
        result = conversions[key](value)
        return f"{value} {from_unit} = {result:.2f} {to_unit}"
    else:
        return f"Conversion from {from_unit} to {to_unit} is not supported."


# Create the agent with tools
agent = Agent(
    model=model,
    system_prompt="You are a helpful AI assistant with access to tools. Use the appropriate tool to answer questions. Be concise.",
    tools=[weather, age_calculator, unit_converter]
)

# --- Test the agent ---

# 1. Math (uses built-in reasoning — no calculator tool needed for simple math)
print("=" * 50)
response = agent("What is 42 * 17?")
print(f"🧮 Math: {response}")

# 2. Weather (uses the custom weather tool)
print("=" * 50)
response = agent("What is the current weather in Chennai?")
print(f"🌤️ Weather: {response}")

# 3. Age calculator (uses the custom age_calculator tool)
print("=" * 50)
response = agent("How old is someone born on January 15, 2000?")
print(f"🎂 Age: {response}")

# 4. Bonus: Unit conversion (uses the custom unit_converter tool)
print("=" * 50)
response = agent("Convert 100 km to miles")
print(f"📏 Conversion: {response}")

# 5. Bonus: Multi-tool question
print("=" * 50)
response = agent("What is the weather in Delhi, and convert the temperature from Celsius to Fahrenheit?")
print(f"🌡️ Multi-tool: {response}")
