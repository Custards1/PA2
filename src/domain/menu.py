#TODO call client functions
from domain import user,client
class Menu:
    def __init__(self,user=None,host=None,port=None,create_user = True):
        self.startup(user,host,port,create_user)
    def startup(self,user,host,port,create_user = True):
        self._is_ok = False
        self._client = None
        if host is not None and port is not None and user is not None:
            try:
                self._client = client.Client(host,port,user,create_user)
                self._is_ok = True
            except:
                pass
    def print_menu(self):
        print("1. Connect to server\n2. Login\n3. Send Message\n4. Print Received Messages\n5. Disconnect")
        if not self._is_ok:
            print("Not connected")
            return None
        return True
    def run_menu(self):#remove client and user perams and create them in the function

        choice = 0
        while choice != 5:
            a = self.print_menu()
            choice = int(input())
            if a is None and choice != 1:
                print("You must connect to a server first!")
                continue
            if choice == 1:#connect to the server
                host = input("Hostname: ")
                port = int(input("Port: "))
                name = input("username: ")
                password = input("password: ")
                display_name = input("display_name: ")
                create_user = input("Enter 1 to create new user, anything else to just login: ")
                create_user = create_user == "1"
                self.startup(user.User(name,password,display_name),host,port)
                pass
            elif choice == 2:
                print("What is your username?")
                username = input()
                print("What is your password?")
                password = input()
                self._client.login()#pass argument
            elif choice == 3:
                print("Who are you messaging?")
                username_to = input()
                print("What is your message?")
                message = input()
                self._client.send_message(username_to, message)
            elif choice == 4:
                self._client.print_pending()
            elif choice == 5:
                self._client.drop()
                self._is_ok = False
            else:
                print("Not a valid option")
