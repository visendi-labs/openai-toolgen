A super simple tool to generate tool specification for the openai API.

## Install
`pip install openai-toolgen`

## Example
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

## Features

### Enums
If the type of an argument is [enum.Enums](https://docs.python.org/3/library/enum.html#enum.Enum) it will be properly serialized according to [openai's spec](https://platform.openai.com/docs/api-reference/chat/create).
```python
>>> from openai_toolgen import tool
>>> from enum import Enum
>>> class Unit(str, enum):
...   celcius = "c"
...   farenheit = "f",
...
>>> @tool
...def get_temperature(unit: unit): pass
...
>>> tool.export_all()[0]['function']['parameters']['properties']
{
  'unit':
  {
    'type': 'string',
    'description': '',
    'enum': ['c', 'f']
  }
}
```

### Parameter descriptions
It is possible to use typing.Annotated to provide a description to the LLM:
```python
>>> from openai_toolgen import tool
>>> from typing import Annotated
>>> @tool
... def foo(bar:Annotated[str, "description of bar"]): pass
...
>>> tool.export_all()[0]['function']['parameters']['properties']
{
  'bar':
  {
    'type': 'string',
    'description': 'description of bar'
  }
}
```
