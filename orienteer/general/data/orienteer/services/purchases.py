from datetime import timezone, datetime, timedelta
from uuid import UUID

from orienteer.general.data.orienteer.repositories import purchases
from orienteer.general.data.products.base_product import BaseProduct
from ..database import async_session


async def create_purchase(user_id: UUID, product_id, product_price):
    async with async_session() as db_session:
        purchase = await purchases.create_purchase(db_session, product_id, user_id, product_price)
        return purchase


async def get_purchase_cooldown(user_id: UUID, product: BaseProduct) -> timedelta | None:
    if product.cooldown is None:
        return None

    async with async_session() as db_session:
        purchase = await purchases.get_last_purchase_of_product(db_session, user_id, product.id)

        if purchase is None:
            return None

        if (product.cooldown + purchase.date) > datetime.now(timezone.utc):
            return (product.cooldown + purchase.date) - datetime.now(timezone.utc)
        else:
            return None
