from sqlalchemy import delete, insert, select, update

from api.supervisor.exceptions import ERROR200, ERROR201, ERROR204
from api.user.models import Supervised, User
from api.user.utils import generate_code
from database import database


async def accept_invitation(user: User, code: str):
    select_query = select(User).where(User.invitation == code)
    supervisor = await database.fetch_one(select_query)
    if supervisor is None:
        raise ERROR201
    if supervisor.id == user.id:
        raise ERROR204

    already_supervised_query = select(Supervised).where(
        Supervised.supervisor_id == supervisor.id,
        Supervised.supervised_id == user.id,
    )
    already_supervised = bool(await database.fetch_one(already_supervised_query))
    if already_supervised:
        raise ERROR200

    update_query = (
        update(User)
        .where(User.id == supervisor.id)
        .values(invitation=await generate_code())
    )
    insert_query = insert(Supervised).values(
        supervisor_id=supervisor.id, supervised_id=user.id
    )

    await database.execute(insert_query)
    await database.execute(update_query)

    # TODO: Notificaciones
    # self.send_notification(NewSupervisorMessage(supervisor=supervisor))
    # supervisor.send_notification(NewSupervisedMessage(supervised=self))


async def get_supervisors(user: User):
    query = select(User).where(
        Supervised.supervised_id == user.id, User.id == Supervised.supervisor_id
    )
    supervisors = await database.fetch_all(query)
    return supervisors


async def get_supervised(user: User):
    query = select(User).where(
        Supervised.supervisor_id == user.id, User.id == Supervised.supervised_id
    )
    supervised = await database.fetch_all(query)
    return supervised


async def delete_supervisor(supervisor_id: str, user: User) -> bool:
    delete_query = delete(Supervised).where(
        Supervised.supervisor_id == supervisor_id,
        Supervised.supervised_id == user.id,
    )
    await database.execute(delete_query)
    return True


async def delete_supervised(supervised_id: str, user: User) -> bool:
    delete_query = delete(Supervised).where(
        Supervised.supervisor_id == user.id,
        Supervised.supervised_id == supervised_id,
    )
    await database.execute(delete_query)
    return True
