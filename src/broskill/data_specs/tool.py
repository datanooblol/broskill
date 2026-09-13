from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

DTYPE_MAP = {
    str: "string",
    int: "integer",
    float: "number",
    bool: "boolean",
}

@dataclass
class Arg:
    name:str = field(
        metadata={"description": "the argument's name, taken from its dest in get_args()"}
    )
    type:Any = field(
        metadata={"description": "the argument's Python type (e.g. str, int) from get_args(), converted to its JSON-schema type string (e.g. 'string', 'integer') on init"}
    )
    description:str | None = field(
        metadata={"description": "the argument's help text, taken from get_args()"},
        default=None
    )
    required:bool | None = field(
        metadata={"description": "whether the argument is required to call the tool"},
        default=True
    )

    def __post_init__(self):
        """Resolve `type` to its JSON-schema string, if given as a Python type.

        Raises:
            ValueError: If `type` is a Python type not in `DTYPE_MAP`.
        """
        if isinstance(self.type, str):
            return
        if self.type not in DTYPE_MAP:
            raise ValueError(f"Unsupported type for arg '{self.name}': {self.type}")
        self.type = DTYPE_MAP[self.type]

@dataclass
class Tool:
    name:str = field(
        metadata={"description": "the tool's name, taken from the script's filename"}
    )
    description:str = field(
        metadata={"description": "the tool's description, taken from get_args()'s parser description"}
    )
    args:list[Arg] = field(
        metadata={"description": "the tool's arguments"}
    )
    path:Path = field(
        metadata={"description": "the path to the script that implements this tool"}
    )
