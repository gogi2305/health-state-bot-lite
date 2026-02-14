from dataclasses import dataclass
from typing import List

@dataclass
class User:
    id: int
    age: int = 0
    goal: str = ""
    activity_level: str = ""  # low/medium/high
    history: List[dict] = None
    
    def __post_init__(self):
        if self.history is None:
            self.history = []
