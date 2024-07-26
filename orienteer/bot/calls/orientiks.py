from disnake import Interaction
from disnake.ui import View, Button
from datetime import datetime, timedelta

from orienteer.bot.utils import embeds
from orienteer.bot.utils.content_locale import Errors, Results, Success, Debug

from orienteer.general.data.products.base_product import Product
from orienteer.general.formatting.time import *

from orienteer.general.data.orienteer.services import discord_auth, orientiks, purchases
from orienteer.general.data.products import products
from orienteer.general.data.ss14.services import player, playtime, bans, seen_time, admin_rank, whitelist, chars

from .abstract import AbstractCall


class Balance(AbstractCall):
    async def __call__(self, ckey: str | None) -> None:
        if ckey is not None:
            ckey = ckey.replace(' ', '')

            user_id = await player.get_user_id(ckey)

            if user_id is None:
                await self.interaction.edit_original_message(embed=embeds.error_message(
                    content=Errors.no_user_id_with_ckey.value))
                return
        else:
            user_id = await discord_auth.get_user_id_by_discord_user_id(self.interaction.user.id)
            if user_id is None:
                await self.interaction.edit_original_message(embed=embeds.error_message(
                    content=Errors.no_user_id_with_discord.value))
                return
            ckey = await player.get_ckey(user_id)

        await self.interaction.edit_original_message(embed=embeds.result_message(title=f'Баланс {ckey}:', content=f'{await orientiks.get_balance(user_id)} <:orienta:1250903370894671963>\'s'))


class Transfer(AbstractCall):
    async def __call__(self, recipient_ckey: str, amount: int) -> None:
        recipient_ckey = recipient_ckey.replace(' ', '')

        recipient_user_id = await player.get_user_id(recipient_ckey)

        amount = int(amount)
        if amount <= 0:
            await self.interaction.edit_original_message(
                embed=embeds.error_message(content=Errors.incorrect_amount.value))

        if recipient_user_id is None:
            await self.interaction.edit_original_message(
                embed=embeds.error_message(content=Errors.recipient_not_found.value))
            return

        if await player.get_discord_user_id_by_user_id(recipient_user_id) is None:
            await self.interaction.edit_original_message(
                embed=embeds.error_message(content=Errors.recipient_not_authorized.value))
            return

        sender_user_id = await discord_auth.get_user_id_by_discord_user_id(self.interaction.user.id)
        if sender_user_id is None:
            await self.interaction.edit_original_message(
                embed=embeds.error_message(content=Errors.no_user_id_with_discord.value))
            return
        sender_ckey = await player.get_ckey(sender_user_id)

        if await orientiks.get_balance(sender_user_id) < amount:
            await self.interaction.edit_original_message(
                embed=embeds.error_message(content=Errors.not_enough_money.value))
            return

        if await orientiks.get_balance(recipient_user_id) < amount:
            await self.interaction.edit_original_message(
                embed=embeds.error_message(content=Errors.you_can_not_transfer_to_account_with_negative_balance.value))
            return

        if sender_user_id == recipient_user_id:
            await self.interaction.edit_original_message(
                embed=embeds.error_message(content=Errors.you_can_not_transfer_to_yourself.value))
            return

        await orientiks.do_transfer(sender_user_id, recipient_user_id, amount)

        await self.interaction.edit_original_message(
            embed=embeds.success_message(Success.transfer.value, f'Баланс получателя ({recipient_ckey}): {await orientiks.get_balance(recipient_user_id)}\n'
                                         f'Баланс отправителя ({sender_ckey}): {await orientiks.get_balance(sender_user_id)}'))


class Shop(AbstractCall):
    async def __call__(self):
        user_id = await discord_auth.get_user_id_by_discord_user_id(self.interaction.user.id)
        if user_id is None:
            await self.interaction.edit_original_message(embed=embeds.error_message(content=Errors.no_user_id_with_discord.value))
            return

        embed = embeds.result_message(title='Товары, доступные к покупке:')
        button_view = View()

        products_array = products.get_all_products()

        def create_callback(product: Product):
            async def buy(interaction: Interaction):
                responding_user_id = await discord_auth.get_user_id_by_discord_user_id(interaction.user.id)

                button_view.clear_items()

                if responding_user_id != user_id:
                    await self.interaction.edit_original_message(
                        embed=embeds.error_message(content=Errors.not_shop_owner.value), view=button_view)
                    return

                if not (await product.can_buy(responding_user_id)):
                    await self.interaction.edit_original_message(
                        embed=embeds.error_message(content=Errors.not_have_permissions.value), view=button_view)
                    return

                purchase_cooldown = await purchases.get_purchase_cooldown(responding_user_id, product)
                if purchase_cooldown is not None:
                    await self.interaction.edit_original_message(
                        embed=embeds.error_message(content=f'{Errors.product_is_in_cooldown_for.value} {get_formatted_timedelta(purchase_cooldown)}'), view=button_view)
                    return

                price = await product.calculate_price(user_id)
                if await orientiks.get_balance(responding_user_id) < price:
                    await self.interaction.edit_original_message(
                        embed=embeds.error_message(content=Errors.not_enough_money.value), view=button_view)
                    return

                product_info = f'{
                    product.description}\n**Цена:** {price} {product.price_tag}'

                await product.buy(responding_user_id)
                await purchases.create_purchase(responding_user_id, product.id, price)
                await orientiks.spent(responding_user_id, price)

                await self.interaction.edit_original_message(
                    embed=embeds.error_message(title=f'{Results.you_have_bought_product.value} **{product.name}**:',
                                               content=product_info), view=button_view)
            return buy

        i = 1
        for product in products_array:
            if not (await product.can_buy(user_id)) or await purchases.get_purchase_cooldown(user_id, product) is not None:
                continue

            i += 1
            price = await product.calculate_price(user_id)
            product_info = f'{
                product.description}\n**Цена:** {price} {product.price_tag}'
            embed.add_field(name=f'{product.emoji} {
                            product.name}', inline=False, value=product_info)

            button = Button(label=product.name, row=i //
                            2, emoji=product.emoji)
            button.callback = create_callback(product)
            button_view.add_item(button)

            await self.interaction.edit_original_message(embed=embed, view=button_view)

        if i == 1:
            await self.interaction.edit_original_message(embed=embeds.error_message(content=Errors.empty_shop.value), view=button_view)
