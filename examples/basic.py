from typing import Annotated
from enum import Enum
import json
from openai import OpenAI
from openai_toolgen import tool

class Unit(str, Enum):
    Celcius = "c"
    Farenheit = "f"

@tool("Call this function when the user wants to know the temperature")
def get_temperature(
        location: Annotated[str, "Location to fetch the tempereature from"],
        unit: Annotated[Unit, "Temperature will be returned in this unit"] = Unit.Celcius
    ):
    return { "temperature": 32, "unit": unit.value, "location": location }

client = OpenAI()
messages = [{"role": "user", "content": "What's the temperature in Stockholm today?"}]
completion = client.chat.completions.create(
    model="gpt-4o",
    messages=messages,
    tools=tool.export_all(),
    tool_choice="required"
)
f = completion.choices[0].message.tool_calls[0].function
print(f"function name: {f.name}")
print(f"function args: {f.arguments}")
res = globals()[f.name](**json.loads(f.arguments))
print(res)
