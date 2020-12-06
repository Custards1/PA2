import socket
from domain import user, parser, base_message
import threading
class BaseClient(threading.Thread):
    def __init__(self,host,port):
        super().__init__()
        self._is_connected = False
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
    def send(self,msg):
        try:
            self._socket.send((msg.replace("\n","")+'\n').encode())
            return True
        except:
            self.drop()
            return False
    @property
    def is_connected(self):
        return self._is_connected
class RelayClient(BaseClient):
    def __init__(self,host,port,user : user.User):
        super().__init__(host,port)
        self._user = user
        self._pending = list()
        self._lock = threading.Lock()
        if not self.login_relay():
            print("Failed loggin in")
            self.drop()
    def login_relay(self):
        if not self.send(parser.build_raw_response_from_list("RUSR",[self._user.name])):
            return False
        msg  = self.get_input()
        if msg is None or msg != "0|Ok":
            return False
        return True
    def clear_pending(self):
        with self._lock:
            self._pending.clear()
    def get_pending_messages(self)->[]:
        with self._lock:
            return self._pending
    def add_to_pending(self,msg):
        with self._lock:
            self._pending.append(msg)

    def run(self):
        while True:
            msg = self.get_input()
            if msg is not None:
                (tag,args) = parser.parse_header(msg)
                if tag == "R":
                    a = base_message.Message()
                    if a.from_tag(args) != 3:
                        if not self.send(parser.build_raw_response(1,"ERR")):
                            break
                    else:
                        self.add_to_pending(a)
                        if not self.send(parser.build_raw_response(0,"OK")):
                            break
                elif tag == "0K":
                    if not self.send(parser.build_raw_response(0,"Ok")):
                        break
                else:
                    if not self.send(parser.build_raw_response(1,"Bad Request")):
                        break
            else:
                break



class Client(BaseClient):
    def __init__(self,host,port,user : user.User,create_user=True):
        super().__init__(host,port)
        self._user = user
        self.login(create_user)
        self._relay = RelayClient(host,port,self._user)
        self._relay.daemon = True
        self._relay.start()

    def make_user(self):
        #Make a USR|..|..|.. request
        if not self.send(parser.build_raw_response_from_list("USR", [self._user.name, self._user.password,
                                                                     self._user.display_name])):
            raise ValueError
        #get input
        msg = self.get_input()
        if msg is None:
            print("msg is None")
            raise ValueError
        (tag, args) = parser.parse_header(msg)
        if tag != "0":
            print(args)
            raise ValueError
        #validate the input is what you wantm
        # this function parses it for you parser.parse_header
        pass
    def login_as_user(self):
        #Make a log request
        #get input,
        #validate input
        if not self.send(parser.build_raw_response_from_list("LOG", [self._user.name, self._user.password])):
            raise ValueError
        msg = self.get_input()
        if msg is None:
            print("msg is None")
            raise ValueError
        (tag, args) = parser.parse_header(msg)
        if tag == "1":
            print("Invalid credentials")
            raise ValueError
        if tag == "2":
            print("Already logged in")
            raise ValueError
        pass
    def login(self,create_user = True):
        #TODO implement login, throw error on failure
        if create_user == True:
            return self.make_user()
        else:
            return self.login_as_user()
        #on error throw error
        pass
    def send_message(self, user_to, msg):
        #Send a MSG|..|..|.. request
        #get input
        #validate input
        #raise error if one
        if not self.send(parser.build_raw_response_from_list("MSG", [self._user.name, user_to, msg])):
            raise ValueError
        msg = self.get_input()
        if msg is None:
            print("msg is None")
            raise ValueError
        (tag, args) = parser.parse_header(msg)
        if tag == "1":
            print("no source user")
            raise ValueError
        if tag == "2":
            print("no target user")
            raise ValueError
        pass
    def print_pending(self):
        msgs = self._relay.get_pending_messages()
        #print out msgs thread safely
        pass
    def drop(self):
        self._relay.drop()
        self._relay.join()
        super().drop()
