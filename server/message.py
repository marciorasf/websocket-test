import json
from collections import defaultdict
from dataclasses import dataclass
from typing import Dict, Literal, Optional, Type, TypeVar, Union

T = TypeVar("T", bound="Message")


@dataclass
class Message:
    action: Union[Literal["subscribe"], Literal["unsubscribe"]]
    payload: Optional[Dict]

    def to_json(self) -> str:
        return json.dumps({"action": self.action, "payload": self.payload})

    @classmethod
    def from_json(cls: Type[T], raw_data: Dict) -> T:
        data = defaultdict(lambda: None, raw_data)
        return Message(action=data["action"], payload=data["payload"])  # type: ignore
