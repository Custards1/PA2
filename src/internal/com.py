from domain import parser
from internal import suser, vault, message
import socket
import threading
from queue import Queue

addr = 8084


class CommunicationNode(threading.Thread):
    def __init__(self, socket=None, hooks=None, user_data=None,connected_user=None):
        super().__init__()
        if socket is None:
            self._is_connected = False
        else:
            self._is_connected = True
        self._socket = socket
        self.connected_user = connected_user
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
        self.add_hook("RUSR", noop)
        self.add_hook("MSG", message.Message.build)

    def is_user(self, user):
        return self.connected_user == user

    def get_input(self):
        print("getting input")
        line = bytes()
        while True:
            part = None
            try:
                print("Before")
                part = self._socket.recv(1)
                print("After ok", part)
            except:
                print("After", part)
                self._is_connected = False
                break
            if part is None or part == b'':
                print("After", part)
                self._is_connected = False
                break
            else:
                if part != b'\n':
                    line += part
                elif part == b'\n':
                    break
        print("Gotten input", line)
        return line.decode('utf-8')

    def drop_connection(self):
        print("Dropping connection")
        try:
            self._socket.close()
            return True
        except:
            self._is_connected = False;
            return False

    def _send(self, msg):
        a = (msg.replace('\n', '') + '\n').encode()
        print("In send ", a)
        try:
            self._socket.send(a)
            print("sent", msg)
            return True
        except:
            self._is_connected = False;
            return False

    def add_hookable(self, hookable):
        self._hooks[hookable[0]] = hookable[1]

    def add_hook(self, hook_key, hook, after_hook=None):
        self._hooks[hook_key] = (hook, after_hook)

    def run_hook(self, hook, args):
        if hook in self._hooks:
            (hooke, _) = self._hooks[hook]
            b = hooke(self, args)
            if b is not None:
                (a, b, (c, d)) = b
                return (a, b, (c, d))
        return (None, None, (None, None))

    def run_after_hook(self, hook, args):
        if hook in self._hooks:
            (_, hooke) = self._hooks[hook]
            if hooke is not None:
                return hooke(self.user_data, args, self)
            return True
        return False

    def _parse(self, msg: str):
        it = 0
        (hook, args) = parser.parse_header(msg)
        print(str(hook))
        print("hook =", hook, ",args =", args)
        (a, b, (c, d)) = self.run_hook(str(hook), [str(ele) for ele in args])
        print("a =", a, ",b =", b, ",c =", c, ",d =", d)
        if c is not None and d is not None:
            if not self._send(parser.build_raw_response(c, d)):
                print("Failed to send")
                self.drop_connection()
                return False
        else:
            print("doppin")
            self.drop_connection()
            return False
        print("doppinvv", b)
        if b == True:
            print("doppinvv start", b)
            if not self.run_after_hook(hook, a):
                print("doppin edn")
                self.drop_connection()
                print("doppin edn")
                return False
            print("gooddf")
            return True
        return True

    def parse(self, msg: str):
        for line in msg.splitlines(keepends=False):
            return self._parse(line)

    def run(self):
        while self._is_connected:
            inv = self.get_input()
            if inv is not None:
                print("", inv)
                self.parse(inv)
        print("")
        self.drop_connection()


class CommunicationNodeRelay(CommunicationNode):
    def __init__(self, socket=None, hooks=None, user_data=None,username = None):
        super().__init__(socket, hooks, user_data)
        self._pending = Queue()
        self._lock = threading.Lock()
        self._runnable = True
        self._username= username

    def add_pending(self, msg, to_user):
        print("Addin pendin")
        with self._lock:
            self.user_data.get(to_user).history.append(msg)

    def get_pending(self):
        print("Addin pendin")
        with self._lock:
            return self.user_data[self.connected_user].history

    def any_pending(self) -> bool:
        print("Addin pendin")
        with self._lock:
            return len(self.user_data[self.connected_user].history) != 0

    def clear_pending(self):
        print("Addin pendin")
        with self._lock:
            self.user_data[self.connected_user].history = list()

    def set_ok(self, ok):
        self._runnable = ok
        if self._runnable == False:
            self.drop_connection()

    def run(self):
        print("meesa waitins baskins")
        while self._runnable:
            msg = self.get_input()
            if msg is None:
                break
            (tag,args) = parser.parse_header(msg)
            if tag == "RUSR":
                self._username=args[0]
                self._send(parser.build_raw_response(0,"Ok"))
            print("meesa waitins")
            while len(ab := self.user_data.get(self._username).history) == 0 and self._runnable:
                pass
            if not self._runnable:
                break
            msg = ab.pop()
            print("sending fra pending",msg)
            self._send(parser.build_raw_response_from_list("R", [str(msg.usr_from), str(msg.id), str(msg.msg)]))

    def drop_connection(self):
        self._runnable = False
        super().drop_connection()

def decifer_communication(sock, user_data,threads_list):
    first_msg = sock.recv(4, socket.MSG_PEEK)
    print("Decifer",user_data,first_msg)
    a = None
    if first_msg == b'RUSR':
        print("Makin relayt")
        a = CommunicationNodeRelay(socket=sock, hooks=None, user_data=user_data)
    else:
        a = CommunicationNode(socket=sock, hooks=None, user_data=user_data)
    a.daemon = True
    a.start()
    threads_list.append(a)


def noop(_, _v):
    return (None, False, (0, "Ok"))


if __name__ == "__main__":
    # create an INET, STREAMing socket
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # bind the socket to a public host, and a well-known port
    serversocket.bind((socket.gethostname(), addr))
    # become a server socket
    serversocket.listen(5)
    (sock, _) = serversocket.accept()
    sock.setblocking(True)
    a = CommunicationNode(socket=sock)

    a.run()
