from http import HTTPStatus
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from vidaplus.models.models import Estoque, BaseUser
from vidaplus.schemas.estoques_schema import (
    EstoqueSchema,
    EstoqueSchemaPublic,
    EstoqueList,
)
from sqlalchemy import select
from typing import Annotated
from vidaplus.security import (
    get_current_user,
)
from vidaplus.database import get_session
from vidaplus.schemas.schemas import FilterPage

router = APIRouter()
Session = Annotated[Session, Depends(get_session)]
CurrentUser = Annotated[BaseUser, Depends(get_current_user)]


@router.post(
    '/',
    status_code=HTTPStatus.CREATED,
    response_model=EstoqueSchemaPublic,
)
def create_estoque(
    estoque: EstoqueSchema,
    session: Session,
    current_user: CurrentUser,
):
    db_estoque = session.scalar(
        select(Estoque).where(Estoque.nome == estoque.nome)
    )

    if db_estoque:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='Item de estoque já existe.',
        )
    
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail='Apenas usuários com permissão de administrador podem criar itens de estoque.',
        )
    
    db_estoque = Estoque(
        tipo_item=estoque.tipo_item,
        nome=estoque.nome,
        quantidade=estoque.quantidade,
        unidade=estoque.unidade,
        data_validade=estoque.data_validade,
    )
    session.add(db_estoque)
    session.commit()
    session.refresh(db_estoque)

    return db_estoque


@router.get(
    '/',
    status_code=HTTPStatus.OK,
    response_model=EstoqueList,
)
def list_estoques(
    session: Session,
    filter_leitos: Annotated[FilterPage, Query()],
    current_user: CurrentUser,
):
    db_estoques = session.scalars(
        select(Estoque)
        .offset(filter_leitos.offset)
        .limit(filter_leitos.limit)
    ).all()

    if not current_user.is_superuser:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail='Apenas usuários com permissão de administrador podem listar itens de estoque.',
        )

    return {'estoques': db_estoques}


@router.get(
    '/{estoque_id}',
    response_model=EstoqueSchemaPublic,
)
def get_estoque(
    estoque_id: int,
    session: Session,
    current_user: CurrentUser,
):
    db_estoque = session.get(Estoque, estoque_id)

    if not db_estoque:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Item de estoque não encontrado.',
        )
    
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail='Apenas usuários com permissão de administrador podem acessar detalhes do item de estoque.',
        )

    return db_estoque

@router.put(
    '/{estoque_id}',
    response_model=EstoqueSchemaPublic,
)
def update_estoque(
    estoque_id: int,
    estoque: EstoqueSchema,
    session: Session,
    current_user: CurrentUser,
):
    db_estoque = session.get(Estoque, estoque_id)

    if not db_estoque:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Item de estoque não encontrado.',
        )
    
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail='Apenas usuários com permissão de administrador podem atualizar itens de estoque.',
        )

    db_estoque.tipo_item = estoque.tipo_item
    db_estoque.nome = estoque.nome
    db_estoque.quantidade = estoque.quantidade
    db_estoque.unidade = estoque.unidade
    db_estoque.data_validade = estoque.data_validade

    session.commit()
    session.refresh(db_estoque)

    return db_estoque