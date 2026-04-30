from abc import ABC, abstractmethod


class BaseMessageBroker(ABC):
    
    @abstractmethod
    async def send_message(self, key: str, topic: str, value: bytes) -> None:
        ...
        
    @abstractmethod
    async def start(self):
        ...
        
    @abstractmethod    
    async def close(self):
        ...
    
    @abstractmethod
    async def start_consuming(self, topic: str):
        ...

    @abstractmethod
    async def stop_consuming(self, topic: str):
        ...
    
