
from infra.repositories.filters.messages import (
    GetAllChatsFilters as GetAllChatsInfraFilters,
)
from infra.repositories.filters.messages import (
    GetMessagesFilters as GetMessagesInfraFilters,
)
from pydantic import BaseModel


class GetAllChatsFilters(BaseModel):
    limit: int = 10
    offset: int = 0
    
    def to_infra(self):
        return GetAllChatsInfraFilters(limit=self.limit, offset=self.offset)


class GetMessagesFilters(BaseModel):
    limit: int = 10
    offset: int = 0

    def to_infra(self):
        return GetMessagesInfraFilters(limit=self.limit, offset=self.offset)