from enum import Enum


class VKEventType(Enum):
    MessageNew = 'message_new'
    MessageReply = 'message_reply'
    MessageTypingState = 'message_typing_state'
    Unknown = ''


class VKEvent:
    def __init__(self, msg: dict):
        try:
            self.type = VKEventType(msg['type'])
        except ValueError:
            self.type = VKEventType.Unknown

        self.group_id = msg['group_id']

        obj = msg['object']

        self.from_id = obj['from_id']
        self.text = ''
        self.date = -1
        self.id = -1
        self.chat_id = -1

        if self.type == VKEventType.MessageNew or self.type == VKEventType.MessageReply:
            self.id = obj['id']
            self.date = obj['date']
            self.text: str = obj['text']
            self.to_chat = self.from_id != obj['peer_id']
            if self.to_chat:
                self.chat_id = obj['peer_id']
                self.id = obj['conversation_message_id']

        self.msg_to_me = False
        if self.type == VKEventType.MessageNew:
            if obj['peer_id'] < 2000000000:
                self.msg_to_me = True
            else:
                group_call = f'[club{self.group_id}|@cyberkotsenko]'
                if self.text.startswith(group_call):
                    self.msg_to_me = True
                    self.text = self.text[len(group_call):]
                    if len(self.text) != 0:
                        self.text = self.text[1:]

    def __str__(self):
        res = ''
        for k, v in self.__dict__.items():
            res += f'{k}: {v}\n'
        return res[:-1]
