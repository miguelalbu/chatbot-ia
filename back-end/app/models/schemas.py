from pydantic import BaseModel
from typing import Optional

class UserMessage(BaseModel):
    message: str
    session_id: Optional[str] = "usuario_padrao"

class BotResponse(BaseModel):
    response: str
    source: str = "AI_Assistant"