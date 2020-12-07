from internal import com, vault
import threading
import socket


class Server:
    def __init__(self, host=socket.gethostname(), port=8080, backlog=100, user_data=vault.Vault()):
        self._host = host
        self._port = port
        print("Starting with addr:",self._host,"on port",self._port)
        self._backlog = backlog
        self._socket = None
        self._go = False
        self._user_data = user_data
        self._threads = list()
    def stop(self):

        try:
            self._socket.close()
        except:
            self._socket = None
        for i in self._threads:
            try:
                i.drop_connection()
            except:
                pass
            try:
                i.join()
            except:
                pass
        self._go = False
    def _start(self):
        self._go = True
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.bind((self._host, self._port))
        self._socket.listen(self._backlog)
        while self._go:
            (con, addr) = self._socket.accept()
            print("Got sum on", addr,self._user_data)
            t = threading.Thread(target=com.decifer_communication, args=(con, self._user_data,self._threads,))
            t.start()
    def start(self):
        if not self._go:
            a = threading.Thread(target=self._start)
            a.daemon = True
            a.start()
            return a
        return None
if __name__ == "__main__":
    coms = Server(port=8094)
    b = None
    while True:
        choice = int(input("1. Load data from file\n2. Start the messenger service\n3. Stop the messenger service\n4. Save data to file\n5. Exit\n>> "))
        if choice == 1:
            pass
        elif choice == 2:
            b = coms.start()
        elif choice == 3:
            coms.stop()
            b = None
        elif choice == 4:
            pass
        elif choice == 5:
            coms.stop()
            b = None
            break
