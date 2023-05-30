import random
import string

from sqlalchemy import select

from api.user.models import User
from database import database


async def generate_code() -> str:
    """
    Genera un código de 10 caracteres y comprueba que no exista en la base de datos
    """

    def generate() -> str:
        code_parts = []
        for length in [3, 4, 3]:
            code_parts.append("".join(random.choices(string.ascii_uppercase, k=length)))
        return "-".join(code_parts).upper()

    async def is_code_repeated(code_to_check) -> bool:
        select_query = select(User).where(User.invitation == code_to_check)
        user = await database.execute(query=select_query)
        return bool(user)

    code: str = generate()
    while await is_code_repeated(code):
        code = generate()

    return code
