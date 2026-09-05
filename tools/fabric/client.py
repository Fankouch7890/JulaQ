import httpx
import os
from typing import Optional, Dict, Any

FABRIC_BASE_URL = "https://api.fabric.foundation/api/core"

class FabricClient:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("FABRIC_API_KEY")
        self.headers = {
            "Content-Type": "application/json"
        }
        if self.api_key:
            self.headers["Authorization"] = f"Bearer {self.api_key}"

    async def send_action(self, robot_id: str, action: str, params: Dict[str, Any] = None) -> Dict:
        """إرسال أمر لروبوت على شبكة Fabric"""
        url = f"{FABRIC_BASE_URL}/robots/{robot_id}/action"
        payload = {
            "action": action,
            "params": params or {}
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=payload, headers=self.headers)

            if response.status_code == 402:
                # هنا سيتم التعامل مع الدفع لاحقاً
                return {"status": "payment_required", "message": "يحتاج دفع عبر RoboPay"}

            response.raise_for_status()
            return response.json()
