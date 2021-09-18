import json
from dataclasses import dataclass
from typing import Dict, Literal, Union


@dataclass
class Message:
    action: Union[Literal["subscribe"], Literal["unsubscribe"]]
    payload: Dict

    def to_json(self) -> str:
        return json.dumps({"action": self.action, "payload": self.payload})
