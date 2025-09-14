import socket

HOST = ("127.0.0.1", 7777)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.connect(HOST)

try:
    # data = sock.recv(1024)
    name_client = "Вася".encode()#input(f"{data}: ").encode()
    # sock.send()
    # name_client = input("Введите своё имя: ").encode()
    sock.send(name_client)
    data = sock.recv(1024).decode()
    print(f"\n{data}\n")
finally:
    print("\n-----Отключение клиента-----")
    sock.close()
