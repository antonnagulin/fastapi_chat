from domain.exeptions.base import ApplicationExeption
from fastapi import Depends, HTTPException, status
from fastapi.routing import APIRouter
from logic.commands.messages import CreateChatCommand, CreateMessageCommand
from logic.init import init_cotainer
from logic.mediator import Mediator
from punq import Container

from application.api.massages.schemas import (
    CreateChatInSchema,
    CreateChatOutSchema,
    CreateMessageInSchema,
    CreateMessageOutSchema,
)
from application.api.schemas import ErrorSchema

router = APIRouter(tags=["Chat"])


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    description="Эндпоинт создает новый чат, если чат с таким названием существует, то возвращается 400 ошибка",  # noqa: E501
    responses={
        status.HTTP_201_CREATED: {"model": CreateChatOutSchema},
        status.HTTP_400_BAD_REQUEST: {"model": ErrorSchema},
    },
)
async def create_chat_handler(
    schema: CreateChatInSchema, container=Depends(init_cotainer)
):
    """ Добавить новый чат """
    mediator: Mediator = container.resolve(Mediator)

    try:
        chat, *_ = await mediator.handle_command(CreateChatCommand(title=schema.title))
    except ApplicationExeption as exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail={"error": exception.massage}
        )

    return CreateChatOutSchema.from_entity(chat)


@router.post(
    '/{chat_oid}/messages',
    status_code=status.HTTP_201_CREATED,
    description='Эндпоинт для добавления нового сообщения в чат с переданным OID',
    responses={
        status.HTTP_201_CREATED: {'model': CreateMessageOutSchema},
        status.HTTP_400_BAD_REQUEST: {'model': ErrorSchema},
    },
)
async def create_message_handler(
    chat_oid: str,
    schema: CreateMessageInSchema,
    container: Container = Depends(init_cotainer),
)-> CreateMessageOutSchema:
    """ Добавить новое сообщение в чат """
    
    mediator: Mediator = container.resolve(Mediator)
    try:
        message, *_ = await mediator.handle_command(
            CreateMessageCommand(text=schema.text, chat_oid=chat_oid)
        )
    except ApplicationExeption as exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={'error': exception.massage}
        )
    
    return CreateMessageOutSchema.from_entity(message)
    