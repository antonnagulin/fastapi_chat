
from dataclasses import dataclass


@dataclass(frozen=True)
class Notification:
    text: str
    title: str
