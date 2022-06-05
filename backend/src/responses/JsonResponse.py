from sanic.response import json
from typing import Dict

class JsonSuccessResponse:
    @classmethod
    def create(self, status: str) -> Dict:
        return json({"status": status, "code": 200})
        
