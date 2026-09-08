import asyncio
from typing import Optional, Dict, Any
from langchain_core.tools import tool
from tools.fabric.robot_control import RobotController

controller = RobotController()

@tool
async def move_robot(
    robot_id: str,
    direction: str = "forward",
    speed: float = 1.0,
    distance: Optional[float] = None,
) -> Dict[str, Any]:
    """
    تحريك الروبوت المحدد باتجاه وسرعة ومسافة معينة عبر شبكة Fabric.

    المعاملات:
      robot_id: معرف الروبوت (مثال: 'robot_01').
      direction: اتجاه الحركة ('forward', 'backward', 'left', 'right').
      speed: سرعة الحركة.
      distance: المسافة بالمراد تحريكها (اختياري).
    """
    return await controller.move(
        robot_id=robot_id,
        direction=direction,
        speed=speed,
        distance=distance,
    )

@tool
async def stop_robot(robot_id: str) -> Dict[str, Any]:
    """
    إيقاف الروبوت المحدد بشكل فوري.

    المعاملات:
      robot_id: معرف الروبوت.
    """
    return await controller.stop(robot_id=robot_id)

@tool
async def get_robot_status(robot_id: str) -> Dict[str, Any]:
    """
    جلب حالة الروبوت الحالية والمعلومات التشغيلية الخاصة به.

    المعاملات:
      robot_id: معرف الروبوت.
    """
    return await controller.get_status(robot_id=robot_id)

@tool
async def execute_fabric_action(
    robot_id: str,
    action: str,
    params: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    تنفيذ إجراء مخصص على روبوت محدد في شبكة Fabric.

    المعاملات:
      robot_id: معرف الروبوت.
      action: اسم الإجراء المراد تنفيذه (مثل: 'lift', 'scan', 'charge').
      params: قاموس المعاملات الإضافية للإجراء.
    """
    return await controller.send_action(robot_id=robot_id, action=action, params=params)

ALL_TOOLS = [move_robot, stop_robot, get_robot_status, execute_fabric_action]
