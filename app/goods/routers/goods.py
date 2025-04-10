from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database.db import get_session
from app.goods.models.goods import Goods, GoodsCreate, GoodsUpdate

router = APIRouter(
    prefix="/goods",
    tags=["goods"],
    responses={404: {"description": "Not found"}},
)


@router.post("/", response_model=Goods, status_code=status.HTTP_201_CREATED)
async def create_goods(
    goods: GoodsCreate, session: AsyncSession = Depends(get_session)
):
    db_goods = Goods(**goods.model_dump())
    session.add(db_goods)
    await session.commit()
    await session.refresh(db_goods)
    return db_goods


@router.get("/", response_model=List[Goods])
async def read_goods(
    skip: int = 0, limit: int = 100, session: AsyncSession = Depends(get_session)
):
    query = select(Goods).offset(skip).limit(limit)
    result = await session.execute(query)
    return result.scalars().all()


@router.get("/{goods_id}", response_model=Goods)
async def read_goods_by_id(goods_id: int, session: AsyncSession = Depends(get_session)):
    query = select(Goods).where(Goods.id == goods_id)
    result = await session.execute(query)
    goods = result.scalar_one_or_none()
    if goods is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Goods not found"
        )
    return goods


@router.put("/{goods_id}", response_model=Goods)
async def update_goods(
    goods_id: int, goods: GoodsUpdate, session: AsyncSession = Depends(get_session)
):
    query = select(Goods).where(Goods.id == goods_id)
    result = await session.execute(query)
    db_goods = result.scalar_one_or_none()
    if db_goods is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Goods not found"
        )

    goods_data = goods.model_dump(exclude_unset=True)
    for key, value in goods_data.items():
        setattr(db_goods, key, value)

    await session.commit()
    await session.refresh(db_goods)
    return db_goods


@router.delete("/{goods_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_goods(goods_id: int, session: AsyncSession = Depends(get_session)):
    query = select(Goods).where(Goods.id == goods_id)
    result = await session.execute(query)
    db_goods = result.scalar_one_or_none()
    if db_goods is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Goods not found"
        )

    await session.delete(db_goods)
    await session.commit()
    return None
