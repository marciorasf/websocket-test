import json
from dataclasses import dataclass
from datetime import datetime
from typing import Union


@dataclass
class Response:
    stream: str
    content: Union[int, str]
    timestamp: datetime

    def to_json(self) -> str:
        return json.dumps(
            dict(
                stream=self.stream,
                content=self.content,
                timestamp=datetime.isoformat(self.timestamp),
            )
        )
