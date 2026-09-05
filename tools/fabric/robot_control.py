from .client import FabricClient

fabric = FabricClient()

async def control_fabric_robot(robot_id: str, action: str, params: dict = None) -> str:
    """
    يتحكم في روبوت على شبكة Fabric.
    
    أمثلة على الاستخدام:
    - action = "move_forward"
    - action = "turn_left"
    - action = "stop"
    - action = "pick_item"
    """
    try:
        result = await fabric.send_action(robot_id, action, params)
        return f"تم تنفيذ الأمر بنجاح على الروبوت {robot_id}: {result}"
    except Exception as e:
        return f"حدث خطأ أثناء التواصل مع Fabric: {str(e)}"
