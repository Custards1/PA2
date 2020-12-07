class User: #define users
    def __init__(self, name=None, password=None, display_name=None, history=None):
        self._name = name
        self._password = password
        self._display_name = display_name
        if history is None:
            self._history = list()
        else:
            self._history = history
        self._logged_in = False
    def as_dct(self):
        return dict(name=self.name,password=self.password,display_name=self.display_name,history=self.history)
    @property
    def logged_in(self):
        return self._logged_in

    @property
    def name(self):
        return self._name

    @property
    def password(self):
        return self._password

    @property
    def display_name(self):
        return self._display_name

    @property
    def history(self):
        return self._history

    @name.setter
    def name(self, msg: str):
        self._name = msg

    @password.setter
    def password(self, msg: str):
        self._password = msg

    @display_name.setter
    def display_name(self, msg: str):
        self._display_name = msg

    @logged_in.setter
    def logged_in(self, boolean: bool):
        self._logged_in = boolean

    @history.setter
    def history(self, msg):
        self._history = msg

