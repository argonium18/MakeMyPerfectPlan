from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime

@dataclass
class Task:
    id: int
    name: str
    duration: int
    cp_estimated_start_time: Optional[datetime] = None
    cp_estimated_end_time: Optional[datetime] = None
    actual_start_time: Optional[datetime] = None
    actual_end_time: Optional[datetime] = None
    target_end_time: Optional[datetime] = None
    difference: Optional[int] = None
    predecessors: List[int] = field(default_factory=list)