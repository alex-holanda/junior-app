import logging
from typing import Annotated

from fastapi import APIRouter, Depends

from app.database import client_table, database
from app.models.client import Client, ClientIn
from app.models.user import User
from app.security import get_current_user

logger = logging.getLogger(__name__)

router = APIRouter(tags=["Client"], prefix="/client")


@router.post("", response_model=Client, status_code=201)
async def create_client(
    client: ClientIn, current_user: Annotated[User, Depends(get_current_user)]
):
    logger.info("Create client")

    data = {**client.model_dump(), "user_id": current_user.id}

    query = client_table.insert().values(data)
    logger.debug(query)

    last_record_id = await database.execute(query)

    return {"id": last_record_id, **data}


@router.get("", response_model=list[Client])
async def get_clients(current_user: Annotated[User, Depends(get_current_user)]):
    logger.info("Get all clients")
    query = client_table.select().where(client_table.c.user_id == current_user.id)
    logger.debug(query)
    return await database.fetch_all(query)
