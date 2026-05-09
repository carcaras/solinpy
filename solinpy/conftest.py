import urllib.request

import pytest


@pytest.fixture(autouse=True)
def block_network_rpc_calls(
    monkeypatch: pytest.MonkeyPatch, request: pytest.FixtureRequest
) -> None:
    """Prevent accidental real RPC network access in unit tests."""
    if request.node.get_closest_marker("integration"):
        return

    def _blocked_urlopen(*args: object, **kwargs: object) -> None:
        raise AssertionError(
            "Outbound RPC/network call blocked in unit tests. "
            "Use RPCMockTransport, monkeypatch urllib.request.urlopen, or mark test as integration."
        )

    monkeypatch.setattr(urllib.request, "urlopen", _blocked_urlopen)
