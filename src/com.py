from domain import parser
import suser
import vault
import socket
import threading
from queue import Queue
addr = 8084
class CommunicationNode(threading.Thread):
    def __init__(self,socket=None,hooks = None,user_data=None):
        super().__init__()
        if socket is None:
            self._is_connected = False
        else:
            self._is_connected = True
        self._socket = socket
        self.connected_user = None
        if hooks is None:
            self._hooks = dict()
        else:
            self._hooks = hooks
        if user_data is None:
            self.user_data = vault.Vault()
        else:
            self.user_data = user_data
        self.add_hook(suser.SUser.tag, suser.SUser.build, vault.Vault.user_creation_hook)
        self.add_hook(vault.Vault.login_tag, vault.Vault.build_login_user)
    def is_user(self,user):
        return self.connected_user == user
    def get_input(self):
        print("getting input")
        line = bytes()
        while True:
            part = None
            try:
                print("Before")
                part = self._socket.recv(1)
                print("After ok",part)
            except:
                print("After",part)
                self._is_connected = False
                break
            if part is None or part == b'':
                print("After",part)
                self._is_connected = False
                break
            else:
                if part != b'\n':
                    line+=part
                elif part == b'\n':
                    break
        print("Gotten input",line)
        return line.decode('utf-8')
    def drop_connection(self):
        print("Dropping connection")
        try:
            self._socket.close()
            return True
        except:
            self._is_connected = False;
            return False
    def _send(self,msg):
        a  =(msg.replace('\n','') + '\n').encode()
        print("In send ",a)
        try:
            self._socket.send(a)
            print("sent",msg)
            return True
        except:
            self._is_connected = False;
            return False

    def add_hookable(self,hookable):
        self._hooks[hookable[0]] =hookable[1]
    def add_hook(self,hook_key,hook,after_hook=None):
        self._hooks[hook_key] =(hook,after_hook)
    def run_hook(self,hook,args):
        if hook in self._hooks:
            (hooke,_) = self._hooks[hook]
            (a,b,(c,d)) =hooke(self,args)
            return (a,b,(c,d))
        return (None,None,(None,None))
    def run_after_hook(self,hook,args):
        if hook in self._hooks:
            (_,hooke) = self._hooks[hook]
            if hooke is not None:
                return hooke(self.user_data,args,self)
            return True
        return False
    def _parse(self,msg : str):
        it = 0
        (hook,args) = parser.parse_header(msg)
        print(str(hook))
        print("hook =",hook,",args =",args)
        (a,b,(c,d)) = self.run_hook(str(hook),[str(ele) for ele in args])
        print("a =",a,",b =",b,",c =",c,",d =",d)
        if c is not None and d is not None:
           if not self._send(parser.build_raw_response(c, d)):
               print("Failed to send")
               self.drop_connection()
               return False
        else:
            print("doppin")
            self.drop_connection()
            return False
        print("doppinvv",b)
        if b == True:
            print("doppinvv start",b)
            if not self.run_after_hook(hook,a):
                print("doppin edn")
                self.drop_connection()
                print("doppin edn")
                return False
            print("gooddf")
            return True
        return False
    def parse(self,msg:str):
        for line in msg.splitlines(keepends=False):
            return self._parse(line)
    def run(self):
        while self._is_connected:
            inv = self.get_input()
            if inv is not None:
                print("",inv)
                self.parse(inv)
        print("")
        self.drop_connection()
class CommunicationNodeRelay(CommunicationNode):
    def __init__(self,socket=None,hooks = None,user_data=None):
        super.__init__(socket,hooks,user_data)
        self._pending = Queue()
        self._lock = threading.Lock()
    def add_pending(self,msg,to_user):
        with self._lock:
            self.user_data.get(to_user).history.append(msg)
    def get_pending(self):
        with self._lock:
            return self.user_data[self.connected_user].history
    def any_pending(self) ->bool:
        with self._lock:
            return len(self.user_data[self.connected_user].history) != 0
    def clear_pending(self):
        with self._lock:
            self.user_data[self.connected_user].history = list()
def decifer_communication(sock,user_data):
    first_msg = sock.recv(4, socket.MSG_PEEK)
    a = None
    if first_msg == "RUSR":
        a = CommunicationNodeRelay(socket=sock,hooks=None,user_data=user_data)
    else:
        a = CommunicationNode(socket=sock,hooks=None,user_data=user_data)
    a.start()
    a.join()

if __name__ == "__main__":
# create an INET, STREAMing socket
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# bind the socket to a public host, and a well-known port
    serversocket.bind((socket.gethostname(), addr))
# become a server socket
    serversocket.listen(5)
    (sock,_ )= serversocket.accept()
    sock.setblocking(True)
    a = CommunicationNode(socket=sock)

    a.run()

