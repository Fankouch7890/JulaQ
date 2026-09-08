import asyncio
import logging
from typing import Optional, Dict, Any

from .client import FabricClient

logger = logging.getLogger(__name__)
_fabric: Optional[FabricClient] = None


def _get_fabric_client() -> FabricClient:
    """Lazy factory for a FabricClient instance.

    Keeps a module-level client that is only created when first needed which
    makes testing (injecting a fake client) easier.
    """
    global _fabric
    if _fabric is None:
        _fabric = FabricClient()
    return _fabric


async def control_fabric_robot_structured(
    robot_id: str,
    action: str,
    params: Optional[Dict[str, Any]] = None,
    fabric_client: Optional[FabricClient] = None,
    timeout: float = 10.0,
    retries: int = 0,
    raise_on_error: bool = False,
) -> Dict[str, Any]:
    """
    يرسل أمرًا إلى روبوت على شبكة Fabric ويُعيد نتيجة مُهيكلة.

    المعاملات:
      - robot_id: مُعرّف الروبوت.
      - action: الإجراء المراد تنفيذه.
      - params: معلمات اختيارية للإجراء.
      - fabric_client: إمكانية إدخال FabricClient للاختبارات أو الاستبدال.
      - timeout: مهلة بالثواني لنداء الشبكة لكل محاولة.
      - retries: عدد مرات إعادة المحاولة عند الفشل (افتراضي 0).
      - raise_on_error: إذا كان True سيُرمى الاستثناء النهائي بدلاً من إرجاعه في الحقل "error".

    النتيجة (قاموس):
      {
        "success": bool,
        "robot_id": str,
        "action": str,
        "result": Any | None,
        "error": str | None
      }
    """
    # Basic validation
    if not robot_id or not isinstance(robot_id, str):
        return {
            "success": False,
            "robot_id": robot_id,
            "action": action,
            "result": None,
            "error": "Invalid robot_id",
        }

    if not action or not isinstance(action, str):
        return {
            "success": False,
            "robot_id": robot_id,
            "action": action,
            "result": None,
            "error": "Invalid action",
        }

    client = fabric_client or _get_fabric_client()
    attempt = 0
    last_exc: Optional[Exception] = None

    while True:
        try:
            attempt += 1
            coro = client.send_action(robot_id, action, params)
            result = await asyncio.wait_for(coro, timeout=timeout)
            logger.info("Executed action '%s' on robot %s (attempt %d)", action, robot_id, attempt)
            return {
                "success": True,
                "robot_id": robot_id,
                "action": action,
                "result": result,
                "error": None,
            }
        except asyncio.TimeoutError as e:
            last_exc = e
            logger.warning("Timeout on attempt %d for robot %s", attempt, robot_id)
        except Exception as e:
            last_exc = e
            logger.exception("Error on attempt %d for robot %s: %s", attempt, robot_id, str(e))

        if attempt > retries:
            break

        # simple linear backoff
        await asyncio.sleep(0.5 * attempt)

    error_msg = str(last_exc) if last_exc else "Unknown error"
    if raise_on_error:
        # Reraise the last exception (or a RuntimeError if none)
        raise last_exc or RuntimeError(error_msg)

    return {
        "success": False,
        "robot_id": robot_id,
        "action": action,
        "result": None,
        "error": error_msg,
    }


# Backwards-compatible wrapper that preserves the original simple string return
async def control_fabric_robot(robot_id: str, action: str, params: dict = None) -> str:
    """
    Backwards-compatible wrapper around control_fabric_robot_structured.

    This matches the original simple API and returns Arabic text like the
    previous implementation so existing callers don't break immediately.
    """
    structured = await control_fabric_robot_structured(robot_id, action, params)
    if structured.get("success"):
        return f"تم تنفيذ الأمر بنجاح على الروبوت {robot_id}: {structured.get('result')}"
    return f"حدث خطأ أثناء التواصل مع Fabric: {structured.get('error')}"
