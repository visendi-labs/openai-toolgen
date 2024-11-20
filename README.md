A clean way to generate tools to be used with openai projects

Example using Openai Completions:

```python
from typing import Annotated
from enum import Enum
from openai import OpenAI
from openai_toolgen import tool

class Unit(str, Enum):
    Celcius = "c"
    Farenheit = "f"

@tool
def get_temperature(
        location: Annotated[str, "Location to fetch the tempereature from"],
        unit: Annotated[Unit, "Temperature will be returned in this unit"] = Unit.Celcius
    ):
    """Call this function when the user wants to know the temperature"""

    return { "temperature": 32, "unit": unit.value, "location": location }

client = OpenAI()
messages = [{"role": "user", "content": "What's the temperature in Stockholm today?"}]
completion = client.chat.completions.create(
    model="gpt-4o",
    messages=messages,
    tools=tool.export_all(),
    tool_choice="required"
)
```
Check out the tests for more details
