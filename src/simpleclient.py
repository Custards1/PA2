import socket
addr = 8080
def get_input(sock):
        print("getting input")
        line = bytes()
        while True:
            part = None
            try:
                print("Before")
                part = sock.recv(1)
                print("After ok",part)
            except:
                print("After",part)

                break
            if part is None or part == b'':
                print("After",part)

                break
            else:
                if part != b'\n':
                    line+=part
                elif part == b'\n':
                    break
        print("Gotten input",line)
        return line.decode('utf-8')
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((socket.gethostname(),addr))
sock.setblocking(True)
print("sending input:","USR|blake|gggg|custards",sock.send(b"USR|blake|gggg|custards\n"))
print(get_input(sock))
print("sending input:","LOG|blake|gggg",sock.send(b"LOG|blake|gggg\n"))

print(get_input(sock))

