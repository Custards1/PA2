from domain import client, menu, base_message, parser, user

#TODO, make this your main file
if __name__ == "__main__":
    menu = menu.Menu(host=input("host"), port=input("port"))
    menu.run_menu()
