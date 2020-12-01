class User:
    tag = "USR"
    def __init__(self,name=None,password=None,display_name=None,history=None):
        self._name = name
        self._password = password
        self._display_name = display_name
        self._history = history
    @staticmethod
    def build(tag):
        r = User()
        b = r.from_tag(tag)
        return (r,b)

    def from_tag(self,tag):
        i = 0
        for it in tag:
            if i == 0:
                self._name = it
            elif i == 1:
                self._password = it
            elif i ==2:
                self._display_name = it
            else:
                break
            i+=1
        if i == 3:
            return True
        return False

    @property
    def name(self):
        return self._name

