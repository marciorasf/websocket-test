from dataclasses import dataclass
from typing import Dict, Literal, Union


@dataclass
class Message:
    action: Union[Literal["subscribe"], Literal["unsubscribe"]]
    payload: Dict
