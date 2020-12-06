class Message:
    def __init__(self,usr_from=None,usr_to=None,msg=None,id=0):
        self.usr_from = usr_from
        self.usr_to = usr_to
        self.msg = msg
        self.id = id
    def from_tag(self,taga):
        i = 0
        for it in taga:
            if i == 0:
                self.usr_from = it
            elif i == 1:
                self.id = it
            elif i == 2:
                self.msg = it
            else:
                break
            i += 1
        return i
