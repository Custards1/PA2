#TODO call client functions
class Menu:
    def print_menu(self, client, user):
        if client.is_connected():
            print("connected")
            if user.logged_in():
                print(user.name())
            else:
                print("not logged in")
        else:
            print("disconnected")
        print("1. Connect to server\n2. Login\n3. Send Message\n4. Print Received Messages\n5. Disconnect")

    def run_menu(self, client, user):#remove client and user perams and create them in the function
        choice = 0
        while choice != 5:
            self.print_menu(client, user)
            choice = input()
            if choice == 1:#connect to the server
                pass
            elif choice == 2:
                print("What is your username?")
                username = input()
                print("What is your password?")
                password = input()
                client.login()#pass argument
            elif choice == 3:
                print("Who are you messaging?")
                username_to = input()
                print("What is your message?")
                message = input()
                client.send_message(username_to, message)
            elif choice == 4:
                client.print_pending()
            elif choice == 5:
                client.drop()
            else:
                print("Not a valid option")
