import asyncio

from aiokafka import AIOKafkaProducer


async def send_one():
    producer = AIOKafkaProducer(bootstrap_servers='kafka:29092')
    
    
    await producer.start()
    
    try:
        await producer.send_and_wait("test-topic", b"Super-pooper message")
    finally:
        await producer.stop()

asyncio.run(send_one())