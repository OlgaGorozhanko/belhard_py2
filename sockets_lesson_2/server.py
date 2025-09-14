import socket


HOST = ("127.0.0.1", 7777)


_method_input = {1: "Войти", 2: "Зарегистрироваться"}


def start() -> str:
    """ Стартовое сообщение от сервера

    :return: Приветственная строка с запросом на выбор метода входа
    """
    return f"\tПриветствую!\nВведите 1.'{_method_input[1]}' либо 2.'{_method_input[2]}'"


def input(metod_input: int):
    if metod_input == 1:
        return_str = "Через клавишу 'enter' Введите Логин и пароль"
    elif metod_input == 2:
        return_str = "Через клавишу 'enter' Введите Имя, возраст, логин и пароль"


def compose_welcome_message(name: str) -> str:
    return f"\nПриветствую {name}! Приятно познакомиться)\nДавай вместе изучать фрэймворки Python)\n"


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.bind(HOST)
sock.listen()
print("-----start server-----")

conn = None
try:
    while True:
        print("-----listen-----")
        conn, addr = sock.accept()
        #print(conn)
        data_name_client = conn.recv(1024).decode()
        print(data_name_client)
        # data_return = compose_welcome_message(data_name_client)
        # conn.send(data_return.encode())
finally:
    if conn:
        print("-----end server-----")
        conn.close()


