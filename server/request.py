import json
from collections import defaultdict
from dataclasses import dataclass
from typing import Any, Dict, Literal, Optional, Type, TypeVar, Union

T = TypeVar("T", bound="Request")


@dataclass
class Request:
    action: Union[Literal["subscribe"], Literal["unsubscribe"]]
    payload: Optional[Dict[str, Any]]

    def to_json(self) -> str:
        return json.dumps({"action": self.action, "payload": self.payload})

    @classmethod
    def from_json(cls: Type[T], raw_data: Dict[str, Any]) -> T:
        data = defaultdict(lambda: None, raw_data)

        if action := data["action"]:
            return Request(action=action, payload=data["payload"])  # type: ignore
        else:
            raise KeyError("Request must have an action.")
