from dataclasses import dataclass, field
from datetime import datetime
from uuid import uuid4

from domain.values.massages import Text, Title


@dataclass
class Massage:
    oid: str = field(default_factory=lambda: str(uuid4()), kw_only=True)

    created_at: datetime = field(
        default_factory=datetime.now,
        kw_only=True,
    )

    text: Text

    def __hash__(self) -> int:
        return hash(self.oid)

    def __eq__(self, __value: "Massage") -> bool:
        return self.oid == __value.oid


@dataclass
class Chat:
    massage: set[Massage] = field(
        default_factory=set,
        kw_only=True,
    )
    oid: str = field(default_factory=lambda: str(uuid4()), kw_only=True)
    title: Title

    created_at: datetime = field(
        default_factory=datetime.now,
        kw_only=True,
    )

    def __hash__(self) -> int:
        return hash(self.oid)

    def __eq__(self, __value: "Chat") -> bool:
        return self.oid == __value.oid

    def add_massage(self, massage: Massage):
        self.massage.add(massage)
