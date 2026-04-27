from aiokafka import AIOKafkaProducer

from infra.message_brokers.base import BaseMessageBroker


class KafkaMessageBroker(BaseMessageBroker):
    producer: AIOKafkaProducer
    
    async def send_message(self, key: str, topic: str, value: bytes)-> None:
        await self.producer.send(topic=topic, key=key, value=value)
    
    async def consume(self, topic: str):        
        ...
