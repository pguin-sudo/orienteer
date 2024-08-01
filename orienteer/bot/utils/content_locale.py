from enum import Enum


class Errors(Enum):
    no_user_id_with_ckey = 'Указанный пользователь не найден.'
    no_user_id_with_discord = 'Ваш аккаунт не привязан к игре.'
    no_playtime_info = 'Не удается найти данные о наигранном времени.'
    recipient_not_found = 'Получатель не найден.'
    recipient_not_authorized = 'Discord аккаунт получателя не привязан к игре.'

    # Orientiks
    incorrect_amount = 'Некорректная сумма.'
    not_enough_money = 'Не достаточно средств.'
    you_can_not_transfer_to_account_with_negative_balance = 'Перевод средств на отрицательные счета запрещен.'
    you_can_not_transfer_to_yourself = 'Нельзя перевести деньги самому себе.'

    # Shop
    empty_shop = 'Похоже, что ваш магазин пуст, приходите завтра :)'
    not_shop_owner = 'Покупки можно совершать только в своем магазине.'
    not_have_permissions = 'Вы не можете совершить эту покупку по неизвестной причине.'
    product_is_in_cooldown_for = 'Вы не можете совершить эту покупку, ещё'

    # Promo
    promo_not_found = 'Такого промокода не существует!'
    promo_used_max_times = 'Промокод уже был использован максимальное количество раз!'
    not_enough_playtime = 'Недостаточно наигранного времени для выполения промокода!'
    promo_overdue = 'Срок промокода истек!'
    promo_used_discord_account = 'Промокод уже был использован от имени этого пользователя!'
    promo_used_ss14_account = 'Промокод уже был использован для этого ckey!'
    creator_promo_used = 'Промокод креатора уже был использован!'

    # Global
    unexpected_error = 'Непредвиденная ошибка'


class Results(Enum):
    no_bans_info = 'Не удается найти данные о банах, скорее всго их нет :).'
    you_have_bought_product = 'Вы приобрели товар'
    you_have_used_promo = 'Промокод успешно использован :)'
    now_you_have_support_creator = 'Теперь вы поддерживаете креатора'
    you_have_received = 'Вы получили:'


class Success(Enum):
    transfer = 'Перевод совершен успешно!'


class Debug(Enum):
    shop_disabled = 'Хуй вам, а не шоп :).'