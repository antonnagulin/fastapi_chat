from domain.exeptions.base import ApplicationExeption
from fastapi import Depends, HTTPException, status
from fastapi.routing import APIRouter
from logic.init import init_cotainer
from logic.commands.messages import CreateChatCommand
from logic.mediator import Mediator

from application.api.massages.schemas import CreateChatInSchema, CreateChatOutSchema
from application.api.schemas import ErrorSchema

router  = APIRouter(tags=['Chat'])

@router.post(
    '/',
    status_code=status.HTTP_201_CREATED,
    description='Эндпоинт создает новый чат, если чат с таким названием существует, то возвращается 400 ошибка',
    responses={
        status.HTTP_201_CREATED: {'model': CreateChatOutSchema},
        status.HTTP_400_BAD_REQUEST: {'model': ErrorSchema},
    },
)
async def create_chat_handler(
    schema: CreateChatInSchema,
    container=Depends(init_cotainer)
):
    mediator: Mediator = container.resolve(Mediator)
    
    try:
        chat, *_ = await mediator.handle_command(CreateChatCommand(title=schema.title))
    except ApplicationExeption as exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={'error': exception.massage}
        )    
    
    return CreateChatOutSchema.from_entity(chat)