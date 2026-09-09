import pytest
from aiohttp.test_utils import AioHTTPTestCase, unittest_run_loop
from server import create_app

class ServerTestCase(AioHTTPTestCase):

    async def get_application(self):
        return create_app()

    @unittest_run_loop
    async def test_health_check(self):
        resp = await self.client.request("GET", "/api/health")
        assert resp.status == 200
        data = await resp.json()
        assert data["status"] == "ok"
        assert "JulaQ" in data["app"]

    @unittest_run_loop
    async def test_robots_list(self):
        resp = await self.client.request("GET", "/api/robots")
        assert resp.status == 200
        data = await resp.json()
        assert "robots" in data
        assert len(data["robots"]) == 4

    @unittest_run_loop
    async def test_robot_move(self):
        resp = await self.client.request("POST", "/api/robot/move", json={"robot_id": "robot_1"})
        assert resp.status == 200
        data = await self.client.request("GET", "/api/robots")
        robots = (await data.json())["robots"]
        r1 = next(r for r in robots if r["robot_id"] == "robot_1")
        assert r1["status"] == "moving"

    @unittest_run_loop
    async def test_robot_stop(self):
        resp = await self.client.request("POST", "/api/robot/stop", json={"robot_id": "robot_1"})
        assert resp.status == 200
        data = await self.client.request("GET", "/api/robots")
        robots = (await data.json())["robots"]
        r1 = next(r for r in robots if r["robot_id"] == "robot_1")
        assert r1["status"] == "stopped"

    @unittest_run_loop
    async def test_chat_endpoint(self):
        resp = await self.client.request("POST", "/api/chat", json={"message": "حرك robot_1"})
        assert resp.status == 200
        data = await resp.json()
        assert "reply" in data
        assert len(data["reply"]) > 0
