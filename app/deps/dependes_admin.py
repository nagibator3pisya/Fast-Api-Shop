from fastapi import Depends, HTTPException
from starlette import status

from app.api.auth import get_current_user
from app.model.models import User


async def get_current_admin_user(
    current_user: User = Depends(get_current_user)
):
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="У вас нет прав для выполнения этой операции"
        )
    return current_user