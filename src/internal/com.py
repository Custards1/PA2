from domain import parser
from internal import suser, vault, message
import socket
import threading
from queue import Queue


#Node to communicate with client
class CommunicationNode(threading.Thread):
    #loads communication node with data
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
    #checks if another user is the connected user
    def is_user(self, user):
        return self.connected_user == user
    #gets input from the client
    def get_input(self):

        line = bytes()
        while True:
            part = None
            try:

                part = self._socket.recv(1)

            except:

                self._is_connected = False
                break
            if part is None or part == b'':

                self._is_connected = False
                break
            else:
                if part != b'\n':
                    line += part
                elif part == b'\n':
                    break

        return line.decode('utf-8')
    #drops the conncetion
    def drop_connection(self):

        try:
            self._socket.close()
            return True
        except:
            self._is_connected = False;
            return False
    #sends a message to the client
    def _send(self, msg):
        a = (msg.replace('\n', '') + '\n').encode()

        try:
            self._socket.send(a)

            return True
        except:
            self._is_connected = False;
            return False
    #adds a hook for a specific tag
    def add_hook(self, hook_key, hook, after_hook=None):
        self._hooks[hook_key] = (hook, after_hook)
    #runs a hook for a specific tag with args
    def run_hook(self, hook, args):
        if hook in self._hooks:
            (hooke, _) = self._hooks[hook]
            b = hooke(self, args)
            if b is not None:
                (a, b, (c, d)) = b
                return (a, b, (c, d))
        return (None, None, (None, None))
    #runs a after success hook
    def run_after_hook(self, hook, args):
        if hook in self._hooks:
            (_, hooke) = self._hooks[hook]
            if hooke is not None:
                return hooke(self.user_data, args, self)
            return True
        return False
    #parses and replys to a message
    def _parse(self, msg: str):
        it = 0
        (hook, args) = parser.parse_header(msg)

        (a, b, (c, d)) = self.run_hook(str(hook), [str(ele) for ele in args])

        if c is not None and d is not None:
            if not self._send(parser.build_raw_response(c, d)):
                print("Failed to send")
                self.drop_connection()
                return False
        else:

            self.drop_connection()
            return False

        if b == True:

            if not self.run_after_hook(hook, a):

                self.drop_connection()

                return False

            return True
        return True
    #parses and replys to a first message
    def parse(self, msg: str):
        for line in msg.splitlines(keepends=False):
            return self._parse(line)
    #runs the node
    def run(self):
        while self._is_connected:
            inv = self.get_input()
            if inv is not None:

                self.parse(inv)

        self.drop_connection()

#Communication node for the message relaying
class CommunicationNodeRelay(CommunicationNode):
    def __init__(self, socket=None, hooks=None, user_data=None,username = None):
        super().__init__(socket, hooks, user_data)
        self._pending = Queue()
        self._lock = threading.Lock()
        self._runnable = True
        self._username= username
    #adds message to pending
    def add_pending(self, msg, to_user):

        with self._lock:
            self.user_data.get(to_user).history.append(msg)
    #gets message from pending
    def get_pending(self):

        with self._lock:
            return self.user_data[self.connected_user].history
    #returns if any messages are pending
    def any_pending(self) -> bool:

        with self._lock:
            return len(self.user_data[self.connected_user].history) != 0
    #clears pending messages
    def clear_pending(self):

        with self._lock:
            self.user_data[self.connected_user].history = list()
    #sets if node is ok
    def set_ok(self, ok):
        self._runnable = ok
        if self._runnable == False:
            self.drop_connection()
    #run the node
    def run(self):

        while self._runnable:
            msg = self.get_input()
            if msg is None:
                break
            (tag,args) = parser.parse_header(msg)
            if tag == "RUSR":
                self._username=args[0]
                self._send(parser.build_raw_response(0,"Ok"))

            while len(ab := self.user_data.get(self._username).history) == 0 and self._runnable:
                pass
            if not self._runnable:
                break
            msg = ab.pop()

            self._send(parser.build_raw_response_from_list("R", [str(msg.usr_from), str(msg.id), str(msg.msg)]))

    def drop_connection(self):
        self._runnable = False
        super().drop_connection()
#determin what kind of node to create and start it
def decifer_communication(sock, user_data,threads_list):
    first_msg = sock.recv(4, socket.MSG_PEEK)

    a = None
    if first_msg == b'RUSR':

        a = CommunicationNodeRelay(socket=sock, hooks=None, user_data=user_data)
    else:
        a = CommunicationNode(socket=sock, hooks=None, user_data=user_data)
    a.daemon = True
    a.start()
    threads_list.append(a)


def noop(_, _v):
    return (None, False, (0, "Ok"))


