import aiohttp
from core.config import Webhooks


async def send_webhook(message: str, is_important: bool, webhook_url=Webhooks.ERRORS) -> bool:
    try:
        payload = {
            'content': f'Важная инфа для <@536086033050107914>: ```{message}```'
        } if is_important else {
            'content': f'Функция **{message}** выполнена успешно'
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(webhook_url, json=payload) as response:
                if response.status == 204:
                    print(message)
                    return True
                else:
                    print(f'Не удалось отправить сообщение в Discord. Код состояния: {response.status}')
                    return False
    except aiohttp.ClientResponseError as e:
        print(f'Произошла ошибка при отправке сообщения в Discord: {str(e)}')
        return False
