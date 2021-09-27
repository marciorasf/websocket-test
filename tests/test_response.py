from datetime import datetime

from server.response import Response


def test_to_json() -> None:
    timestamp = datetime.fromisoformat("2021-09-27 21:00:00")
    response = Response(content=1, timestamp=timestamp)

    assert response.content == 1
    assert response.timestamp == timestamp
