import socket
from domain import user, client

cli = client.Client(host=socket.gethostname(),
                    port=8080,
                    user=user.User(name="Blake",
                                   password="1234",
                                   display_name="Custards"))

cli.drop()
