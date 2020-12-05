import domain.base_message as base
class Conversation:
    def __init__(self,usr_from,usr_to):
        self._usr_from = usr_from
        self._usr_to = usr_to
        self._messages = list()
    def add_message(self,message):
        if ((message.usr_from == self._usr_from and message.usr_to == self._usr_to) or (message.usr_from == self._usr_to and message.usr_to == self._usr_from)) and message not in self._messages:
            self._messages.append(message)
            return True
        return False
    @property
    def messages(self):
        return self._messages

    pass

class Message(base.Message):
    ids = 0
    def __init__(self,usr_from,usr_to,msg,id=None):
        super().__init__(usr_from,usr_to,msg)
        if id is None:
            self._id = Message.ids
            Message.ids += 1
        else:
            self._id = id
    @property
    def id(self):
        return self._id
