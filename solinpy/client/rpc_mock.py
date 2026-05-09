import json
from collections import defaultdict
from typing import Any


class _MockHTTPResponse:
    def __init__(self, payload: dict[str, Any]):
        self._payload = payload

    def read(self) -> bytes:
        return json.dumps(self._payload).encode("utf-8")

    def __enter__(self) -> "_MockHTTPResponse":
        return self

    def __exit__(self, exc_type: Any, exc: Any, tb: Any) -> bool:
        return False


class RPCMockTransport:
    """In-memory transport to simulate JSON-RPC responses in offline tests."""

    def __init__(self) -> None:
        self._responses: dict[str, list[dict[str, Any]]] = defaultdict(list)
        self.requests: list[dict[str, Any]] = []

    def queue_result(self, method: str, result: Any) -> None:
        self._responses[method].append({"result": result})

    def queue_error(
        self,
        method: str,
        code: int,
        message: str,
        data: Any | None = None,
    ) -> None:
        error_payload: dict[str, Any] = {"code": code, "message": message}
        if data is not None:
            error_payload["data"] = data
        self._responses[method].append({"error": error_payload})

    def queue_raw(self, method: str, payload: dict[str, Any]) -> None:
        self._responses[method].append(payload)

    def __call__(self, req: Any, timeout: float | None = None) -> _MockHTTPResponse:
        payload = json.loads(req.data.decode("utf-8"))
        method = payload.get("method")
        self.requests.append({"method": method, "params": payload.get("params", []), "timeout": timeout})

        queue = self._responses.get(method, [])
        if not queue:
            raise AssertionError(
                f"RPC mock has no queued response for method '{method}'. "
                "Queue responses with queue_result/queue_error/queue_raw."
            )

        body = {
            "jsonrpc": "2.0",
            "id": payload.get("id"),
            **queue.pop(0),
        }
        return _MockHTTPResponse(body)
