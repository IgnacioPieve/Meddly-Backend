from sqlalchemy import delete, insert, select, update
from starlette.background import BackgroundTasks

from api.notification.models.message import NewSupervisedMessage, NewSupervisorMessage
from api.notification.service import send_notification
from api.supervisor.exceptions import ERROR200, ERROR201, ERROR204
from api.user.models import Supervised, User
from api.user.utils import generate_code
from database import database


async def accept_invitation(user: User, code: str, background_tasks: BackgroundTasks):
    """
    Accepts an invitation from a supervisor.

    Args:
        user (User): The user accepting the invitation.
        code (str): The invitation code.
        background_tasks (BackgroundTasks): Background tasks to be executed.
    """

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

    await send_notification(
        NewSupervisorMessage(
            supervisor=User(**supervisor),
        ),
        user=User(**user),
        background_tasks=background_tasks,
    )
    await send_notification(
        NewSupervisedMessage(
            supervised=User(**user),
        ),
        user=User(**supervisor),
        background_tasks=background_tasks,
    )


async def get_supervisors(user: User) -> list[User]:
    """
    Gets the supervisors of a user.

    Args:
        user (User): The user.

    Returns:
        List[User]: A list of user objects representing the supervisors.
    """

    query = select(User).where(
        Supervised.supervised_id == user.id, User.id == Supervised.supervisor_id
    )
    supervisors = await database.fetch_all(query)
    return supervisors


async def get_supervised(user: User) -> list[User]:
    """
    Gets the supervised users of a supervisor.

    Args:
        user (User): The user (supervisor).

    Returns:
        List[User]: A list of user objects representing the supervised users.
    """

    query = select(User).where(
        Supervised.supervisor_id == user.id, User.id == Supervised.supervised_id
    )
    supervised = await database.fetch_all(query)
    return supervised


async def delete_supervisor(supervisor_id: str, user: User) -> bool:
    """
    Deletes a supervisor from the supervised list.

    Args:
        supervisor_id (str): The ID of the supervisor to delete.
        user (User): The user.

    Returns:
        bool: True if the supervisor was deleted successfully, False otherwise.
    """

    delete_query = delete(Supervised).where(
        Supervised.supervisor_id == supervisor_id,
        Supervised.supervised_id == user.id,
    )
    await database.execute(delete_query)
    return True


async def delete_supervised(supervised_id: str, user: User) -> bool:
    """Deletes a supervised user from the supervisor's list.

    Args:
        supervised_id (str): The ID of the supervised user to delete.
        user (User): The user (supervisor).

    Returns:
        bool: True if the supervised user was deleted successfully, False otherwise.
    """

    delete_query = delete(Supervised).where(
        Supervised.supervisor_id == user.id,
        Supervised.supervised_id == supervised_id,
    )
    await database.execute(delete_query)
    return True
