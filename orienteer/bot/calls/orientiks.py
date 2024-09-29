from datetime import timezone

from disnake import Interaction
from disnake.ui import View, Button
from loguru import logger

from orienteer.bot.calls.abstract import AbstractCall
from orienteer.bot.utils import embeds
from orienteer.bot.utils.content_locale import Errors, Results, Success
from orienteer.general.config import CURRENCY_SIGN, USERS_OWNERS
from orienteer.general.data.orienteer.services import (
    transactions,
    purchases,
)
from orienteer.general.data.products.products.abstract import AbstractProduct
from orienteer.general.data.products.services import get_all_products
from orienteer.general.formatting.player import ping
from orienteer.general.formatting.time import *
from orienteer.general.utils.dtos import UserDTO


class Balance(AbstractCall):
    async def __call__(self, user_dto: UserDTO) -> None:
        await self.interaction.edit_original_message(
            embed=embeds.result_message(
                title=f"Баланс {user_dto.ckey}:",
                content=f"{await transactions.get_balance(user_dto.user_id)} {CURRENCY_SIGN}",
            )
        )


class Transfer(AbstractCall):
    async def __call__(
        self, sender_user_dto: UserDTO, recipient_user_dto: UserDTO, amount: int
    ) -> None:
        amount = int(amount)
        if amount <= 0:
            await self.interaction.edit_original_message(
                embed=embeds.error_message(content=Errors.incorrect_amount.value)
            )
            return

        if recipient_user_dto.discord_user_id is None:
            await self.interaction.edit_original_message(
                embed=embeds.error_message(
                    content=Errors.recipient_not_authorized.value
                )
            )
            return

        if await transactions.get_balance(sender_user_dto.user_id) < amount:
            await self.interaction.edit_original_message(
                embed=embeds.error_message(content=Errors.not_enough_money.value)
            )
            return

        if await transactions.get_balance(recipient_user_dto.user_id) < 0:
            await self.interaction.edit_original_message(
                embed=embeds.error_message(
                    content=Errors.you_can_not_transfer_to_account_with_negative_balance.value
                )
            )
            return

        if sender_user_dto.user_id == recipient_user_dto.user_id:
            await self.interaction.edit_original_message(
                embed=embeds.error_message(
                    content=Errors.you_can_not_transfer_to_yourself.value
                )
            )
            return

        await transactions.do_transfer(
            sender_user_dto.user_id, recipient_user_dto.user_id, amount
        )

        await self.interaction.edit_original_message(
            embed=embeds.success_message(
                Success.transfer.value,
                f"Баланс получателя ({recipient_user_dto.ckey}): {await transactions.get_balance(recipient_user_dto.user_id)}\n"
                f"Баланс отправителя ({sender_user_dto.ckey}): {await transactions.get_balance(sender_user_dto.user_id)}\n",
            )
        )


class Shop(AbstractCall):
    async def __call__(self, user_dto: UserDTO) -> None:
        user_dto = await UserDTO.from_discord_user_id(self.interaction.user.id)
        if user_dto is None:
            await self.interaction.edit_original_message(
                embed=embeds.error_message(content=Errors.no_user_id_with_discord.value)
            )
            return

        embed = embeds.result_message(title="Товары, доступные к покупке:")
        button_view = View()

        products_array = get_all_products()

        def create_callback(product_: AbstractProduct):
            async def buy(interaction: Interaction):
                responding_user_dto = await UserDTO.from_discord_user_id(
                    interaction.user.id
                )

                button_view.clear_items()

                if responding_user_dto != user_dto:
                    await self.interaction.edit_original_message(
                        embed=embeds.error_message(content=Errors.not_shop_owner.value),
                        view=button_view,
                    )
                    return

                if not (await product_.can_buy(responding_user_dto.user_id)):
                    await self.interaction.edit_original_message(
                        embed=embeds.error_message(
                            content=Errors.not_have_permissions_shop.value
                        ),
                        view=button_view,
                    )
                    return

                purchase_cooldown = await purchases.get_purchase_cooldown(
                    responding_user_dto.user_id, product_
                )
                if purchase_cooldown is not None:
                    await self.interaction.edit_original_message(
                        embed=embeds.error_message(
                            content=f"{Errors.product_is_in_cooldown_for.value} {get_formatted_timedelta(purchase_cooldown)}"
                        ),
                        view=button_view,
                    )
                    return

                price_ = await product_.calculate_price(user_dto.user_id)
                if await transactions.get_balance(responding_user_dto.user_id) < price_:
                    await self.interaction.edit_original_message(
                        embed=embeds.error_message(
                            content=Errors.not_enough_money.value
                        ),
                        view=button_view,
                    )
                    return

                product_info_ = (
                    f"{product_.description}\n**Цена:** {price_} {product_.price_tag}"
                )

                await product_.buy(responding_user_dto.user_id)
                await purchases.create_purchase(
                    responding_user_dto.user_id, product_.id, price_
                )
                await transactions.spend(responding_user_dto.user_id, price_)

                await self.interaction.edit_original_message(
                    embed=embeds.success_message(
                        title=f'{Results.you_have_bought_product.value} **"{product_.name}"**:',
                        content=product_info_,
                    ),
                    view=button_view,
                )

            return buy

        i = 1
        for product in products_array:
            if (
                not (await product.can_buy(user_dto.user_id))
                or await purchases.get_purchase_cooldown(user_dto.user_id, product)
                is not None
            ):
                continue

            i += 1
            price = await product.calculate_price(user_dto.user_id)
            product_info = (
                f"{product.description}\n**Цена:** {price} {product.price_tag}"
            )
            embed.add_field(
                name=f"{product.emoji} {product.name}", inline=False, value=product_info
            )

            button = Button(label=product.name, row=i // 2, emoji=product.emoji)
            button.callback = create_callback(product)
            button_view.add_item(button)

            await self.interaction.edit_original_message(embed=embed, view=button_view)

        if i == 1:
            await self.interaction.edit_original_message(
                embed=embeds.error_message(content=Errors.empty_shop.value),
                view=button_view,
            )


class Purchases(AbstractCall):
    async def __call__(self, user_dto: UserDTO):
        user_purchases = await purchases.get_all_user_purchases(user_dto.user_id)
        if user_purchases is None or user_purchases == ():
            await self.interaction.edit_original_message(
                embed=embeds.result_message(
                    f"Покупки {user_dto.ckey}:", content="Отсутствуют"
                )
            )
            return

        embed = embeds.result_message(f"Покупки {user_dto.ckey}:")

        for i, (purchase, product) in enumerate(user_purchases):
            sub_info = ""
            if product.is_subscription:
                if product.cooldown:
                    expire_date = product.cooldown + purchase.date
                    sub_info = (
                        f"Действует до {get_formatted_datetime(expire_date)}"
                        if expire_date > datetime.now(timezone.utc)
                        else f"Подписка истекла {get_formatted_datetime(expire_date)}"
                    )
                else:
                    sub_info = "Бессрочная подписка"

            embed.add_field(
                f"{i + 1}. {product.emoji} {product.name}",
                f"Дата покупки: {get_formatted_datetime(purchase.date)}\n"
                f"Цена: {purchase.price if purchase.price is not None else 'Бесценно'}{product.price_tag if purchase.price is not None else ''}\n"
                f"{sub_info}",
                inline=False,
            )

        await self.interaction.edit_original_message(embed=embed)


class Buy(AbstractCall):
    async def __call__(self, amount: int, user_dto: UserDTO) -> None:
        amount = int(amount)
        if amount <= 0:
            await self.interaction.edit_original_message(
                embed=embeds.error_message(content=Errors.incorrect_amount.value)
            )
            return

        buy_price = await transactions.get_price(buy=True)

        embed = embeds.result_message(
            "Заявка на покупку ориентиков...",
            f"Цена покупки: {int(buy_price * amount)}₽ *({buy_price}₽ за 1 {CURRENCY_SIGN})*",
        )

        button_view = View()

        async def pay_callback(interaction: Interaction):
            if interaction.user.id not in USERS_OWNERS:
                button_view.clear_items()

                await self.interaction.edit_original_message(
                    embed=embeds.success_message(content=Errors.not_have_permissions),
                    view=button_view,
                )

            responding_user_dto = await UserDTO.from_discord_user_id(
                interaction.user.id
            )

            button_view.clear_items()

            if responding_user_dto.user_id != user_dto.user_id:
                await self.interaction.edit_original_message(
                    embed=embeds.error_message(content=Errors.not_shop_owner.value),
                    view=button_view,
                )
                return

            await self.interaction.edit_original_message(
                embed=embeds.success_message(
                    title=Success.transfer.value,
                    content=f"Вы приобрели {amount}{CURRENCY_SIGN} за {int(buy_price * amount)}₽",
                ),
                view=button_view,
            )

            # PRICE CHECK and CHANGE TYPE
            await transactions.add_orientiks_from_boosty(user_dto.user_id, amount)
            logger.info("Orientiks bought")

        dev_button = Button(label="Купить", emoji="💳")
        dev_button.callback = pay_callback
        button_view.add_item(dev_button)

        button = Button(
            label="Перейти на сайт оплаты",
            emoji="💳",
            url="https://google.com",
            disabled=True,
        )
        button_view.add_item(button)

        await self.interaction.edit_original_message(embed=embed, view=button_view)


class Bogachi(AbstractCall):
    async def __call__(self):
        leaderboard = await transactions.get_leaderboard()
        description = ""

        for i, leader in enumerate(leaderboard):
            description += (
                f"{i + 1}. "
                f"**{leader[0].ckey}"
                f"{ping(leader[0].discord_user_id)}:** "
                f"{leader[1]}{CURRENCY_SIGN}\n"
            )

        embed = embeds.result_message("Богачи:", content=description)

        await self.interaction.edit_original_message(embed=embed)
