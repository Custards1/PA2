#TODO call client functions
from domain import user,client
class Menu:
    def __init__(self,user,host,port,create_user = True):
        self._is_ok = False
        self._client = None
        try:
            self._client = client.Client(host,port,user,create_user)
            self._is_ok = True
        except:
            pass

    def print_menu(self):
        if not self._is_ok:
            print("disconnected, invalid connection attempt")
            return None
        print("1. Connect to server\n2. Login\n3. Send Message\n4. Print Received Messages\n5. Disconnect")
        return True
    def run_menu(self):#remove client and user perams and create them in the function

        choice = 0
        while choice != 5:
            if self.print_menu() is None:
                return None
            choice = input()
            if choice == 1:#connect to the server
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
