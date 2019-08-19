# from generator import Generator
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from os import environ
from random import randint, choice
from string import ascii_lowercase

from bot_utils.quotes import get_quote
from bot_utils.ads import get_ad
from generator import Generator

generator = Generator('trained_data/cyber_weights')


def process_command(message: str) -> str:
    is_ad = randint(1, 10) == 1
    if is_ad:
        return get_ad()

    if message.find('цитата') != -1:
        return get_quote()
    else:
        return generator.generate(seed=message, size=randint(10, 80))


def get_random_string(length: int = 10):
    letters = ascii_lowercase
    return ''.join(choice(letters) for _ in range(length))


def write_msg(api, user_id, message):
    api.method('messages.send', {'peer_id': user_id, 'message': message, 'random_id': str(randint(0, 2147483647))})


if __name__ == '__main__':
    try:
        token = environ['API_KEY']
    except:
        exit(1)

    vk = vk_api.VkApi(token=token)
    longpoll = VkLongPoll(vk)

    print('Бот запущен')

    for event in longpoll.listen():
        print(event.type)

        # Если пришло новое сообщение
        if event.type == VkEventType.MESSAGE_NEW:
            if hasattr(event, 'chat_id'):
                chat_id = event.chat_id
            else:
                chat_id = None

            print(event.text)
            # Если оно имеет метку для меня( то есть бота)
            if event.text.find('@cyberkotsenko') != -1 or event.to_me:

                # Сообщение от пользователя
                request: str = event.text

                pos = request.find('@cyberkotsenko')
                if pos != -1:
                    request = request[pos:]
                    request.replace('@cyberkotsenko', '')

                request = request.lower()

                if chat_id is not None:
                    id = 2000000000 + chat_id
                else:
                    id = event.user_id

                # Каменная логика ответа
                response = process_command(request)
                write_msg(vk, id, response)
