import os
import json
import asyncio
from aiohttp import web
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage

from agent import create_julaq_agent
from tools.fabric import RobotController

load_dotenv()

robot_controller = RobotController()

# State store for local active robots
robots_state = {
    "robot_1": {"robot_id": "robot_1", "status": "idle", "battery": 95, "position": [10, 20]},
    "robot_2": {"robot_id": "robot_2", "status": "idle", "battery": 88, "position": [30, 40]},
    "robot_3": {"robot_id": "robot_3", "status": "idle", "battery": 72, "position": [50, 60]},
    "robot_4": {"robot_id": "robot_4", "status": "idle", "battery": 60, "position": [70, 80]},
}

# Cache/Initialize agent app
has_openai_key = bool(os.getenv("OPENAI_API_KEY"))
agent_app = None
if has_openai_key:
    try:
        agent_app = create_julaq_agent()
    except Exception as e:
        print(f"Warning: Could not initialize LangGraph agent: {e}")

async def handle_index(request):
    return web.FileResponse(os.path.join(os.path.dirname(__file__), 'web', 'index.html'))

async def handle_health(request):
    return web.json_response({"status": "ok", "app": "JulaQ Agent Server"})

async def handle_robots_list(request):
    # Try calling fabric for each robot, update local state
    for rid in robots_state.keys():
        res = await robot_controller.get_status(rid)
        if res.get("success") and isinstance(res.get("result"), dict):
            robots_state[rid].update(res["result"])
    return web.json_response({"robots": list(robots_state.values())})

async def handle_robot_move(request):
    try:
        data = await request.json()
    except Exception:
        data = {}
    robot_id = data.get("robot_id", "robot_1")
    res = await robot_controller.move(robot_id)
    if robot_id in robots_state:
        robots_state[robot_id]["status"] = "moving"
    return web.json_response({"status": "moving", "robot_id": robot_id, "fabric_res": res})

async def handle_robot_stop(request):
    try:
        data = await request.json()
    except Exception:
        data = {}
    robot_id = data.get("robot_id", "robot_1")
    res = await robot_controller.stop(robot_id)
    if robot_id in robots_state:
        robots_state[robot_id]["status"] = "stopped"
    return web.json_response({"status": "stopped", "robot_id": robot_id, "fabric_res": res})

async def handle_robot_status(request):
    try:
        data = await request.json()
    except Exception:
        data = {}
    robot_id = data.get("robot_id", "robot_1")
    res = await robot_controller.get_status(robot_id)
    state = robots_state.get(robot_id, {"robot_id": robot_id, "status": "unknown"})
    return web.json_response({"robot_id": robot_id, "status": state["status"], "details": state, "fabric_res": res})

async def handle_chat(request):
    try:
        data = await request.json()
        user_message = data.get("message", "").strip()
    except Exception:
        user_message = ""

    if not user_message:
        return web.json_response({"error": "رسالة فارغة"}, status=400)

    if agent_app and has_openai_key:
        try:
            inputs = {"messages": [HumanMessage(content=user_message)]}
            result = await agent_app.ainvoke(inputs)
            last_msg = result["messages"][-1]
            return web.json_response({"reply": last_msg.content, "mode": "ai"})
        except Exception as e:
            print(f"Chat AI Error: {e}")

    # Fallback when AI key is not available or fails
    words = user_message.split()
    reply = ""
    action_result = None

    if len(words) >= 2 and words[0] in ["حرك", "move"]:
        robot_id = words[1]
        action_result = await robot_controller.move(robot_id)
        if robot_id in robots_state:
            robots_state[robot_id]["status"] = "moving"
        reply = f"تم إرسال أمر التحريك للروبوت ({robot_id}). الحالة: moving"
    elif len(words) >= 2 and words[0] in ["أوقف", "stop"]:
        robot_id = words[1]
        action_result = await robot_controller.stop(robot_id)
        if robot_id in robots_state:
            robots_state[robot_id]["status"] = "stopped"
        reply = f"تم إرسال أمر الإيقاف للروبوت ({robot_id}). الحالة: stopped"
    elif len(words) >= 2 and words[0] in ["حالة", "status"]:
        robot_id = words[1]
        action_result = await robot_controller.get_status(robot_id)
        state = robots_state.get(robot_id, {})
        reply = f"معلومات الروبوت ({robot_id}): الموقع {state.get('position', [0,0])} - البطارية {state.get('battery', 100)}% - الحالة {state.get('status', 'idle')}"
    else:
        reply = f"مرحباً! أنا JulaQ الذكي. استلمت رسالتك: \"{user_message}\". يمكنك تجربة أوامر مثل 'حرك robot_1' أو 'أوقف robot_2' أو 'حالة robot_1'."

    return web.json_response({
        "reply": reply,
        "mode": "fallback",
        "action_result": action_result
    })

def create_app():
    app = web.Application()
    app.router.add_get('/', handle_index)
    app.router.add_get('/api/health', handle_health)
    app.router.add_get('/api/robots', handle_robots_list)
    app.router.add_post('/api/robot/move', handle_robot_move)
    app.router.add_post('/api/robot/stop', handle_robot_stop)
    app.router.add_post('/api/robot/status', handle_robot_status)
    app.router.add_post('/api/chat', handle_chat)

    # Serve static assets under /static
    static_dir = os.path.join(os.path.dirname(__file__), 'web')
    if not os.path.exists(static_dir):
        os.makedirs(static_dir, exist_ok=True)
    app.router.add_static('/static', static_dir)
    return app

if __name__ == '__main__':
    port = int(os.getenv("PORT", 3000))
    app = create_app()
    web.run_app(app, host='0.0.0.0', port=port)
