import json
from dataclasses import dataclass
from typing import Dict, Literal, Type, TypeVar, Union

T = TypeVar("T", bound="Message")


@dataclass
class Message:
    action: Union[Literal["subscribe"], Literal["unsubscribe"]]
    payload: Dict

    def to_json(self) -> str:
        return json.dumps({"action": self.action, "payload": self.payload})

    @classmethod
    def from_json(cls: Type[T], data: Dict) -> T:
        return Message(action=data["action"], payload=data["payload"])  # type: ignore
