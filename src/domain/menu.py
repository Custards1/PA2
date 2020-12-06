#TODO call client functions
from domain import user,client
class Menu:
    def __init__(self,user=None,host=None,port=None,create_user = True):
        self._host = host
        self._port = port
        self.startup(user,create_user)
    def startup(self,user,create_user = True):
        self._is_ok = False
        self._client = None
        if self._host is not None and self._port is not None and user is not None:
            try:
                self._client = client.Client(self._host,self._port,user,create_user)
                self._is_ok = True
            except:
                pass
    def print_menu(self):
        print("1. Connect to server\n2. Login\n3. Send Message\n4. Print Received Messages\n5. Disconnect")
        if not self._is_ok:
            print("Not connected")
            return None
        else:
            print("User:",self._user.display_name)
        return True
    def run_menu(self):#remove client and user perams and create them in the function

        choice = 0
        while choice != 5:
            a = self.print_menu()
            choice = int(input())
            if a is None and (choice != 1 and choice !=2):
                print("You must connect to a server first and log in!")
                continue
            if choice == 1:#connect to the server
                self._host = input("Hostname: ")
                self._port = int(input("Port: "))
                pass
            elif choice == 2:
                print("What is your username?")
                username = input()
                print("What is your password?")
                password = input()
                display_name = input("display_name: ")
                create_user = int(input("Enter 1 to create a new user, anything else to login as existing: ")) == 1
                self.startup(user.User(username,password,display_name),create_user)
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
