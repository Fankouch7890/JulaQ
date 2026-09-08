import pytest
from unittest.mock import AsyncMock, patch
from langchain_core.messages import AIMessage, HumanMessage

from agent.tools import move_robot, stop_robot, get_robot_status, execute_fabric_action, ALL_TOOLS
from agent.agent import create_julaq_agent


@pytest.mark.asyncio
async def test_agent_tools_invocation():
    with patch("agent.tools.controller.send_action", new_callable=AsyncMock) as mock_send:
        mock_send.return_value = {"success": True, "robot_id": "r1", "action": "move", "result": "ok", "error": None}

        res = await move_robot.ainvoke({"robot_id": "r1", "direction": "forward", "speed": 1.5})
        assert res["success"] is True
        mock_send.assert_called_once_with("r1", "move", {"direction": "forward", "speed": 1.5})


@pytest.mark.asyncio
async def test_agent_graph_creation_and_execution():
    agent = create_julaq_agent()
    assert agent is not None

    mock_response = AIMessage(content="أهلاً بك! أنا JulaQ جاهز لمساعدتك.")

    with patch("langchain_openai.ChatOpenAI.ainvoke", new_callable=AsyncMock) as mock_invoke:
        mock_invoke.return_value = mock_response
        inputs = {"messages": [HumanMessage(content="مرحبا")]}
        result = await agent.ainvoke(inputs)
        assert len(result["messages"]) >= 2
        assert result["messages"][-1].content == "أهلاً بك! أنا JulaQ جاهز لمساعدتك."
