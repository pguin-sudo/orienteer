from datetime import timezone, datetime, timedelta
from uuid import UUID

from orienteer.general.data.orienteer.repositories import purchases
from orienteer.general.data.products.abstract_product import AbstractProduct
from ..database import async_session
from ..models.purchases import Purchase
from ...products import products


async def create_purchase(user_id: UUID, product_id, product_price):
    async with async_session() as db_session:
        purchase = await purchases.create_purchase(db_session, product_id, user_id, product_price)
        return purchase


async def get_purchase_cooldown(user_id: UUID, product: AbstractProduct) -> timedelta | None:
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


async def get_current_subscriptions() -> tuple[tuple[Purchase, AbstractProduct], ...]:
    async with async_session() as db_session:
        purchases_ = await purchases.get_all_purchases(db_session)
        result = []
        for purchase in purchases_:
            product = products.get_product(purchase.product_id)
            if (product is None or product.cooldown is None or not product.is_subscription
                    or purchase.date + product.cooldown < datetime.now(timezone.utc)):
                continue
            result.append((purchase, product))
        return tuple(result)


async def get_all_user_purchases(user_id: UUID) -> tuple[tuple[Purchase, AbstractProduct], ...]:
    async with async_session() as db_session:
        purchases_ = await purchases.get_all_purchases_of_user(db_session, user_id)
        result = [] # noqa
        for purchase in purchases_:
            product = products.get_product(purchase.product_id)
            if (product is None or product.cooldown is None or not product.is_subscription
                    or purchase.date + product.cooldown < datetime.now(timezone.utc)):
                continue
            result.append((purchase, product))
        return tuple(result)
