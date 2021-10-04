import json
from collections import defaultdict
from dataclasses import dataclass
from typing import Any, Dict, Literal, Union


@dataclass
class Request:
    action: Union[Literal["subscribe"], Literal["unsubscribe"]]
    stream: str

    def to_json(self) -> str:
        return json.dumps({"action": self.action, "stream": self.stream})

    @classmethod
    def from_json(cls, raw_data: Dict[str, Any]) -> "Request":
        data = defaultdict(lambda: None, raw_data)

        if "action" in data and "stream" in data:
            return Request(action=data["action"], stream=data["stream"])
        else:
            raise KeyError("Both action and stream are required fields.")
