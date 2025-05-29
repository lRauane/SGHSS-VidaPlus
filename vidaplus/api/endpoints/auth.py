from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.orm import Session

from vidaplus.models.models import BaseUser
from vidaplus.schemas.auth_schema import Token
from vidaplus.security import (
    create_access_token,
    get_session,
    verify_password,
    get_current_user
)

router = APIRouter()

Session = Annotated[Session, Depends(get_session)]
CurrentUser = Annotated[BaseUser, Depends(get_current_user)]


@router.post('/', response_model=Token)
def login_for_access_token(
    session: Session,
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    user = session.scalar(
        select(BaseUser).where(BaseUser.email == form_data.username)
    )

    if not user:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail='Incorrect email or password',
        )

    if not verify_password(form_data.password, user.senha):
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail='Incorrect email or password',
        )

    access_token = create_access_token(data={'sub': user.email})

    return {'access_token': access_token, 'token_type': 'bearer'}


@router.post('/refresh_token', response_model=Token)
async def refresh_access_token(user: CurrentUser):
    new_access_token = create_access_token(data={'sub': user.email})

    return {'access_token': new_access_token, 'token_type': 'bearer'}