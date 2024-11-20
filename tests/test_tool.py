from typing import Annotated
from openai_toolgen import Toolbox

def test_tool_two_args():
    tool = Toolbox()
    @tool
    def foo(
        arg1: Annotated[int, "Description about arg1"],
        arg2: Annotated[str, "Description about arg2"]
    ):
        """Description how to use foo"""
        ...
    expected_output = [
        {
            "type": "function",
            "function": { 
                "name": "foo",
                "description": "Description how to use foo",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "arg1": {
                            "type": "number",
                            "description": "Description about arg1"
                        },
                        "arg2": {
                            "type": "string",
                            "description": "Description about arg2"
                        }
                    },
                    "required": ["arg1", "arg2"]
                }
            }
        }
    ]
    assert tool.export_all() == expected_output


def test_tool_with_optional_arg():
    tool = Toolbox() 
    @tool
    def foo(
        arg1: Annotated[int, "Description about arg1"],
        arg2: Annotated[str, "Description about arg2"] = "hej"
    ):
        """Description how to use foo"""
        ...
    assert tool.export_all()[0]['function']['parameters']['required'] == ["arg1"]

def test_tool_with_enum_arg():
    from enum import Enum
    class Unit(str, Enum):
        Celcius = "c"
        Farenheit = "f",
    
    tool = Toolbox()
    @tool
    def get_temperature(unit: Annotated[Unit, "Temperature"]): pass
    assert tool.export_all()[0]['function']['parameters']['properties']['unit']['type'] == 'string'
    assert tool.export_all()[0]['function']['parameters']['properties']['unit']['enum'] == ["c", "f"]
        
