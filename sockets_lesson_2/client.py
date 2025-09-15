import socket

HOST = ("192.168.100.71", 7777)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.connect(HOST)

try:
    choise = input("Выберите:\n\t\t1.Войти\n\t\t2.Зарегестрироваться")
    name_client = input("Введите своё имя: ")
    password_client = input("Введите пароль: ")
    command = "signin" if choise == 1 else "reg"
    data_for_send = f"command:{command};login:{name_client};password:{password_client}".encode()
    sock.send(data_for_send)
    data = sock.recv(1024)
    print(f"\n{data.decode()}\n")
finally:
    print("\n-----Отключение клиента-----")
    sock.close()
