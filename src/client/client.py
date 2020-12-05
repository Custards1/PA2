import socket
from domain import user, parser
class BaseClient:
    def __init__(self,host,port):
        self._is_connected = False
        self._socket.connect((host, port)) #raises error on failure
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.connect((host, port)) #raises error on failure
        self._is_connected = True
    def get_input(self):
        if not self._is_connected:
            return None
        line = bytes()
        while True:
            part = None
            try:
                part = self._socket.recv(1)
            except IOError:
                self.drop()
                break
            if part is None or part == b'':
                self.drop()
                break
            else:
                if part != b'\n':
                    line+=part
                elif part == b'\n':
                    break

        return line.decode('utf-8').strip()
    def drop(self):
        if self._is_connected:
            try:
                self._socket.close()
            except IOError:
                pass
        self._is_connected = False
    def send(self,msg : str):
        try:
            self._socket.send((msg.replace("\n","")+'\n').replace("|","").encode())
            return True
        except:
            self.drop()
            return False
    @property
    def is_connected(self):
        return self._is_connected
class RelayClient(BaseClient):
    def __init__(self,host,port,self_user : user.User):
        super().__init__(host,port)
        self._user = self_user
        self.login_relay()
    def login_relay(self):
        #Ill do this later today
        pass
    def get_pending_messages(self)->[]:
        #Ill do this later today
        pass


class Client(BaseClient):
    def __init__(self,host,port,self_user : user.User,create_user=True):
        super().__init__(host,port)
        self._user = self_user
        self.login(self._user,create_user)
        self._relay = RelayClient(host,port,self_user)

    def login(self,create_user = True):
        #TODO implement login, throw error on failure
        #Dont use this in final, this is just example of what to do
        if not self.send("USR|%s|%s|$s".format(self._user.name,self._user.password,self._user.display_name)):
            raise ValueError
        msg = self.get_input()
        if msg is None:
            raise ValueError
        (tag,args) = parser.parse_header(msg)
        if tag != "0" and args !=["Ok"]:
            raise ValueError
        pass
    def send_message(self):
        #TODO implement login, throw error on failure
        pass
    def print_pending(self):
        #TODO implement print_pending, throw error on failure
        msgs = self._relay.get_pending_messages()
        if msgs is not None:
            while i := msgs.pop() and i is not None:
                print(i)
        pass

