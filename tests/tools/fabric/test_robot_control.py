import asyncio
import pytest

import tools.fabric.robot_control as rc
from tools.fabric.robot_control import control_fabric_robot_structured


@pytest.mark.asyncio
async def test_control_success():
    class FakeClient:
        async def send_action(self, robot_id, action, params):
            return {"status": "ok"}

    client = FakeClient()
    res = await control_fabric_robot_structured("r1", "move", {}, fabric_client=client)
    assert res["success"] is True
    assert res["result"] == {"status": "ok"}


@pytest.mark.asyncio
async def test_timeout_and_retries():
    class FlakyClient:
        def __init__(self):
            self.count = 0

        async def send_action(self, robot_id, action, params):
            self.count += 1
            # sleep longer than the provided timeout for the first two calls
            if self.count < 3:
                await asyncio.sleep(0.05)
                return "late"
            return "ok"

    client = FlakyClient()
    res = await control_fabric_robot_structured("r1", "move", fabric_client=client, timeout=0.01, retries=2)
    assert res["success"] is True
    assert res["result"] == "ok"
    assert client.count == 3


@pytest.mark.asyncio
async def test_raise_on_error():
    class BadClient:
        async def send_action(self, robot_id, action, params):
            raise ValueError("boom")

    client = BadClient()
    with pytest.raises(ValueError):
        await control_fabric_robot_structured("r1", "move", fabric_client=client, retries=0, raise_on_error=True)


@pytest.mark.asyncio
async def test_wrapper_returns_text():
    class FakeClient:
        async def send_action(self, robot_id, action, params):
            return "ok"

    # inject fake client into module-level _fabric so the backwards-compatible wrapper uses it
    rc._fabric = FakeClient()

    msg = await rc.control_fabric_robot("r42", "stop", None)
    assert "تم تنفيذ الأمر بنجاح على الروبوت r42" in msg
