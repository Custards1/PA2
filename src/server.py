from internal import com, vault
import threading
import socket


class Server:
    def __init__(self, host=socket.gethostname(), port=8080, backlog=100, user_data=vault.Vault()):
        self._host = host
        self._port = port
        self._backlog = backlog
        self._socket = None
        self._user_data = user_data
        self._threads = list()

    def start(self):
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.bind((self._host, self._port))
        self._socket.listen(self._backlog)
        while True:
            (con, addr) = self._socket.accept()
            print("Got sum on", addr)
            t = threading.Thread(target=com.decifer_communication, args=(con, self._user_data,))
            self._threads.append(t)
            t.start()


if __name__ == "__main__":
    coms = Server()
    coms.start()
