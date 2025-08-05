from typing import Optional, TypedDict

class AgentState(TypedDict):
    input: Optional[str]
    image: Optional[str]  # base64 image
    output: Optional[str]
