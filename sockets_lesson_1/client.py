import socket

HOST = ("127.0.0.1", 7777)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.connect(HOST)

try:
    name_client = input("Введите своё имя: ").encode()
    sock.send(name_client)
    data = sock.recv(1024)
    print(f"\n{data.decode()}\n")
finally:
    print("\n--Отключение клиента--")
    sock.close()
