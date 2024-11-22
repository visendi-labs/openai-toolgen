from typing import Annotated, Callable, Sequence, get_origin, get_type_hints, get_args
import inspect
import enum
from openai.types.chat import ChatCompletionToolParam

def _map_type(t):
    type_map = {
        int: "number",
        float: "number",
        str: "string",
        bool: "boolean",
        list: "array",
        dict: "object",
        None: "null"
    }
    return type_map.get(t, "string")  # default to string

def _extract_parameter_info(func: Callable) -> dict:
    sig = inspect.signature(func)
    type_hints = get_type_hints(func, globalns=func.__globals__, include_extras=True)
    properties = {}
    required = []
    for param in sig.parameters.values():
        param_name = param.name
        if param.default is inspect.Parameter.empty:
            required.append(param_name)
        annotation = type_hints.get(param_name, None)
        desc = ''
        if annotation:
            if get_origin(annotation) is Annotated:
                base_type, desc = get_args(annotation)
            else:
                base_type = annotation
        else:
            base_type = None
        json_type = _map_type(base_type)
        properties[param_name] = {
            "type": json_type,
            "description": desc
        }
        if isinstance(base_type, enum.EnumMeta):
            properties[param_name]['enum'] = [e.value for e in base_type]
    return {
        "properties": properties,
        "required": required
    }

def _extract_tool_info(func: Callable, desc: str) -> dict:
    parameters = _extract_parameter_info(func)
    return {
        "type": "function",
        "function": {
            "name": func.__name__,
            "description": desc,
            "parameters": {
                "type": "object",
                "properties": parameters['properties'],
                "required": parameters['required']
            }
        }
    }

class Toolbox:
    def __init__(self) -> None:
        self.tools = []

    def __call__(self, *args, **kwargs) -> Callable:
        if len(args) == 1 and callable(args[0]) and not kwargs:
            func=args[0]
            self.tools.append(_extract_tool_info(func, ''))
            return  func
        else:
            desc = args[0] if args else ''
            def decorator(func: Callable):
                self.tools.append(_extract_tool_info(func, desc))
                return func
            return decorator

    def export_all(self) -> Sequence[ChatCompletionToolParam]:
        return self.tools

tool = Toolbox()  # Default
