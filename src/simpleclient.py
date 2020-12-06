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
            return [elem for elem in self._pending]
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

    def login(self,create_user = True):
        #TODO implement login, throw error on failure
        #Dont use this in final, this is just example of what to do
        if not self.send("USR|{}|{}|{}".format(self._user.name,self._user.password,self._user.display_name)):
            raise ValueError
        msg = self.get_input()
        if msg is None:
            raise ValueError
        (tag,args) = parser.parse_header(msg)
        if tag != "0" and args !=["Ok"]:
            raise ValueError
        pass
    def send_message(self,user_to,msg):
        if not self.send(parser.build_raw_response_from_list("MSG",[self._user.name,user_to,msg])):
            raise ValueError
        msg = self.get_input()
        if msg is None:
            print("msg is None")
            raise ValueError
        (tag,args) = parser.parse_header(msg)
        if tag != "0":
            print("tag is",tag,"args:",args)
            raise ValueError
        pass
        pass
    def print_pending(self):
        #TODO implement print_pending, throw error on failure
        msgs = self._relay.get_pending_messages()
        for i in msgs:
            i.usr_to =self._user.name
        self._relay.clear_pending()
        print(msgs)
        pass
    def drop(self):
        super().drop()
        self._relay.drop()
if __name__ == "__main__":
    a = Client(socket.gethostname(),8094,user.User(input("name >> "),input("password >> "),input("display name >> ")))
    print(a.send_message(input("Who >>"),input("What >>")))
    print("sent")
    a.print_pending()
    print("sent pending")
    a.drop()
