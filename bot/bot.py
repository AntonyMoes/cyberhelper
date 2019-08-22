from vk_api import VkApi
from vk_api.longpoll import VkLongPoll, VkEventType
from random import randint

from bot.process import process_command


class Bot:
    def __init__(self, token: str):
        self._vk = VkApi(token=token)
        self._longpoll = VkLongPoll(self._vk)

    def run(self):
        for event in self._longpoll.listen():
            print(event.type)

            if event.type == VkEventType.MESSAGE_NEW:
                # if hasattr(event, 'chat_id'):
                #     chat_id = event.chat_id
                # else:
                #     chat_id = None

                print(event.text)
                # if event.text.find('@cyberkotsenko') != -1 or event.to_me:
                if event.to_me:
                    # request = event.text
                    # pos = request.find('@cyberkotsenko')
                    # if pos != -1:
                    #     request = request[pos:]
                    #     request.replace('@cyberkotsenko', '')
                    # request = request.lower()

                    request = event.text.lower()

                    # if chat_id is not None:
                    #     response_id = 2000000000 + chat_id
                    # else:
                    #     response_id = event.user_id
                    response_id = event.user_id

                    response = process_command(request)
                    self.write_msg(response_id, response)

    def write_msg(self, response_id: int, response: str):
        self._vk.method('messages.send',
                        {'peer_id': response_id, 'message': response, 'random_id': str(randint(0, 2147483647))})
