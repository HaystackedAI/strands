# Challenge 2: Adding Tools to Your Agent ⭐⭐

> Give your agent superpowers by adding a calculator and custom tools using **Amazon Nova Pro** via **Amazon Bedrock**.

---

## 🎯 Goal

Learn how to extend an AI agent with **custom tools** using the Strands Agents SDK. The agent uses Amazon Nova Pro (`amazon.nova-pro-v1:0`) as its foundation model and can invoke tools to perform real-world tasks like fetching weather, calculating age, and converting units.

---

## 📋 Prerequisites

| Requirement | Details |
|-------------|---------|
| AWS Account | With Amazon Bedrock access enabled |
| Amazon Nova Pro | Model must be enabled in your Bedrock console |
| AWS CLI | Credentials configured via `aws configure` |
| Python 3.10+ | Installed on your system |
| pip packages | `strands-agents`, `strands-agents-bedrock`, `requests` |

---

## 🔧 How to Configure Amazon Bedrock (Nova Pro v1)

### Step 1: Enable Model Access in AWS Console

1. Go to the [Amazon Bedrock Console](https://console.aws.amazon.com/bedrock/)
2. Select **us-east-1** (N. Virginia) region from the top-right dropdown
3. In the left sidebar, click **Model access**
4. Click **Modify model access**
5. Find **Amazon Nova Pro** in the list and check the box
6. Click **Next** → **Submit**
7. Wait until the status shows **Access granted** ✅

### Step 2: Configure AWS Credentials

Run the following command and enter your credentials:

```bash
aws configure
```

You'll be prompted for:
```
AWS Access Key ID: <your-access-key>
AWS Secret Access Key: <your-secret-key>
Default region name: us-east-1
Default output format: json
```

### Step 3: Verify Access

Test that your credentials work with Bedrock:

```bash
aws bedrock list-foundation-models --region us-east-1 --query "modelSummaries[?modelId=='amazon.nova-pro-v1:0'].modelId"
```

You should see:
```json
["amazon.nova-pro-v1:0"]
```

### Step 4: Install Python Dependencies

```bash
pip install strands-agents strands-agents-bedrock requests
```

---

## 🧠 How the Model is Configured in Code

```python
from strands.models.bedrock import BedrockModel

model = BedrockModel(
    model_id="amazon.nova-pro-v1:0",
    region_name="us-east-1"
)
```

![Screenshot 2026-05-21 143407.png](https://images.tomarkdown.dev/uploaded/kuh0z3q9pn856zol.png)

| Parameter | Value | Description |
|-----------|-------|-------------|
| `model_id` | `amazon.nova-pro-v1:0` | The Amazon Nova Pro foundation model |
| `region_name` | `us-east-1` | AWS region where Bedrock is available |

The `BedrockModel` class handles all the authentication and API communication with Amazon Bedrock using your configured AWS credentials.

---

## 📚 What You'll Learn

- ✅ How to use the `@tool` decorator to create custom tools
- ✅ How the agent reads **docstrings** to understand tool purpose
- ✅ How **type annotations** tell the agent what parameters to pass
- ✅ How the agent **decides which tool to use** based on the question
- ✅ How to chain **multiple tools** in a single query

---

## 🛠️ Tools in This Challenge

### 1. Weather Tool (`@tool`)

Fetches live weather data from the [wttr.in](https://wttr.in) API.

```python
@tool
def weather(city: str) -> str:
    """Get the current weather for a given city."""
    response = requests.get(f"https://wttr.in/{city}?format=j1")
    ...
```

### 2. Age Calculator Tool (`@tool`)

Calculates age from a birth date using Python's `datetime` module.

```python
@tool
def age_calculator(birth_year: int, birth_month: int, birth_day: int) -> str:
    """Calculate a person's age given their date of birth."""
    ...
```

### 3. Unit Converter Tool (`@tool`) — Bonus

Converts between common units (km/miles, kg/lbs, °C/°F, cm/inches).

```python
@tool
def unit_converter(value: float, from_unit: str, to_unit: str) -> str:
    """Convert a value from one unit to another."""
    ...
```

---

## 🔑 How Tool Selection Works

The agent uses a **reasoning loop**:

1. Receives the user's question
2. Reads all available tool **docstrings** and **parameter types**
3. Decides if a tool is needed (or if it can answer directly)
4. Calls the appropriate tool with the right arguments
5. Returns the tool's output as part of its response

You can see this in the output — the agent's `<thinking>` tags show its decision process:

```
<thinking> I need to use the 'weather' tool to get the current weather... </thinking>
Tool #1: weather
```

---

## ▶️ How to Run

```bash
cd challenge-2-tools
python starter.py
```

---

## ✅ Expected Output

Here's the actual output from running the agent:

### 🧮 Math: `42 * 17`

```
<thinking> The requested calculation does not require any external tools.
I can perform the multiplication directly. </thinking>

The result of 42 * 17 is 714.
```

> The agent recognizes simple math doesn't need a tool — it computes directly.

---

### 🌤️ Weather: Chennai

```
<thinking> I need to use the 'weather' tool to get the current weather
conditions in Chennai. </thinking>

Tool #1: weather
The current weather in Chennai is thundery with outbreaks nearby,
a temperature of 35°C, and humidity at 51%.
```

> The agent calls the `weather` tool with `city="Chennai"` and returns live data.

---

### 🎂 Age: Born January 15, 2000

```
<thinking> I need to use the 'age_calculator' tool to calculate the age
of someone born on January 15, 2000. </thinking>

Tool #2: age_calculator
Someone born on January 15, 2000, is 26 years old.
```

> The agent passes `birth_year=2000, birth_month=1, birth_day=15` to the tool.

---

### 📏 Unit Conversion: 100 km to miles

```
<thinking> I need to use the 'unit_converter' tool to convert
100 kilometers to miles. </thinking>

Tool #3: unit_converter
100 kilometers is approximately 62.14 miles.
```

> The agent calls `unit_converter(value=100, from_unit="km", to_unit="miles")`.

---

### 🌡️ Multi-Tool: Weather + Conversion

```
<thinking> First, I need to get the current weather in Delhi using the
'weather' tool. Then, I'll extract the temperature in Celsius and convert
it to Fahrenheit using the 'unit_converter' tool. </thinking>

Tool #4: weather
<thinking> I have the current weather in Delhi, which is 44°C. Now I need
to convert this temperature from Celsius to Fahrenheit using the
'unit_converter' tool. </thinking>

Tool #5: unit_converter
The current weather in Delhi is sunny with a temperature of 44°C (111.2°F)
and humidity at 9%.
```

> The agent **chains two tools** — first fetches weather, then converts the temperature. This demonstrates multi-tool reasoning.

---


## output:

![Screenshot 2026-05-21 143333.png](https://images.tomarkdown.dev/uploaded/c08x14fjt1tlo5jx.png)


## 🏗️ Project Structure

```
challenge-2-tools/
├── starter.py      # Main agent code with tools
└── README.md       # This file
```

---

## 💡 Key Takeaways

| Concept | How It Works |
|---------|--------------|
| `@tool` decorator | Converts any Python function into an agent-usable tool |
| Docstrings | The agent reads these to understand **when** to use a tool |
| Type annotations | Tell the agent **what parameters** to pass |
| Tool selection | Agent uses reasoning (`<thinking>`) to pick the right tool |
| Multi-tool chaining | Agent can call multiple tools sequentially for complex queries |
| No tool needed | Agent skips tools for simple tasks (like basic math) |

---



## 📎 References

- [Strands Agents SDK](https://github.com/strands-agents/strands-agents)
- [Amazon Bedrock Documentation](https://docs.aws.amazon.com/bedrock/)
- [Amazon Nova Models](https://docs.aws.amazon.com/bedrock/latest/userguide/models-supported.html)
- [wttr.in Weather API](https://wttr.in/:help)
