# PA2
# Status
Works with some minor errors
# Team members
Blake Brown, Elie Schooley
# Description
Client-Server multithreading system for a messaging system
# Files
## src
### Name: client.py
    Description: Main call for client.
### Name: server.py
    Description: Main call for server.
## domain
### Name: base_message.py
    Description: Represents a message
### Name: client.py
    Description: functions for the client class.
### Name: menu.py
    Description: run and print the menu
### Name: parser.py
    Description: formating for protocal
### Name: user.py
    Description: users for the client
## internal
### Name: com.py
    Description: holds communication classes for the server
### Name: message.py
    Description: Holds server representation of a message
### Name: suser.py
    Description: Holds server representation of a user
### Name: vault.py
    Description: Holds all users
# Known bugs
    Sometimes saving to file and loading in the same server process might hang the menu
