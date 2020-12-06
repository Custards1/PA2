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
    def __init__(self,usr_from=None,usr_to=None,msg=None,id=None):
        super().__init__(usr_from,usr_to,msg)
        if id is None:
            self._id = Message.ids
            Message.ids += 1
        else:
            self.id = id
    def from_tag(self,taga):
        i = 0
        for it in taga:
            if i == 0:
                self.usr_from = it
            elif i == 1:
                self.usr_to = it
            elif i == 2:
                self.msg = it
            else:
                break
            i += 1
        return i
    @staticmethod
    def build(vaults,tag):
        r = Message()
        b = r.from_tag(tag) == 3
        if b == True:
            m = vaults.user_data.get(r.usr_to)
            if m is None:
                return (r,b,(1,"INVALID REQUEST"))
            vaults.user_data.get(r.usr_to).history.append(r)
            return (r,b,(0,"OK"))
        return (r,b,(1,"INVALID REQUEST"))



