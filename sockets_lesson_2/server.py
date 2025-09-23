import socket
from datetime import datetime


HOST = ("192.168.100.71", 7777)
conn = None
OK = b"HTTP/1.1 200 OK\n"
HEADERS = b"Host: some.ru\nHost1: some1.ru\nContent-Type: text/html; charset=utf-8\n\n"
ERR_404 = b"HTTP/1.1 404 Not Found\n\n"

clients = {}


def send_file_to_brower(_file_name: str, _conn: socket):
    try:
        with open(_file_name.lstrip('/'), 'rb') as f:
            _conn.send(OK)
            _conn.send(HEADERS)
            _conn.send(f.read())
    except IOError:
        print('нет файла')
        conn.send(ERR_404)


def is_file(path):
    print("is_file(path)")
    if '.' in path:
        ext = path.split(".")[-1]
        if ext in ['jpg', 'jpeg', 'png', 'gif', 'ico', 'txt', 'html', 'json']:
            return True
    return False


def parse_answer(data_answer: str) -> tuple[str | None, str, str | None]:
    """ Разделение первой строки ответа

    :param data_answer:
    :return: tuple[метод передачи, путь]
    """
    if " " in data_answer:
        _method, _path, _ver = data_answer.split('\n')[0].split(" ", 2)  # получаем path из 1ой строки http
        print(f"method -- {_method},\npath -- {_path},\nver -- {_ver}")
        return _method, _path, _ver
    else:
        return None, data_answer, None

def send_text_to_brower(_data: str, _conn: socket):
    conn.send(OK)
    conn.send(HEADERS)
    _http = f"<H1>{_data}</H1>"
    _conn.send(_http.encode())


def check_login_and_password(login: str, password: str) -> bool:
    """ Проверка корректности логина и пароля

    :param login: логин
    :param password: пароль
    :return: True -- корректны, иначе False
    """
    return True if len(login) >= 6 and login.isalnum() and len(password) >= 8 and any(char.isdigit() for char in password) else False


def add_client(login: str, password: str):
    clients[login] = password

def correct_login_pass(login: str, password: str, _conn: socket, datetime_for_send: str):
    """ Действия при корректном прохождении проверки логина и пароля

    :param login:
    :param password:
    :param _conn:
    :return:
    """
    try:
        add_client(login, password)
    except:
        _conn.send(f"Ошибка регистрации пользователя {login}. Попробуйте ещё раз".encode())
    else:
        data_send = f"{datetime_for_send} -- пользователь {login} зарегестрирован"
        _conn.send(data_send.encode())


def incorrect_login_pass(login: str, _conn: socket, datetime_for_send: str):
    """ Действия, если проверка логина и пароля провалена

    :return:
    """
    data_send = f"{datetime_for_send} -- ошибка регистрации {login} - неверный логин/пароль"
    _conn.send(data_send.encode())


def is_client(login: str, password: str) -> bool:
    """ Проверка имеется ли пользователь

    :param login:
    :param password:
    :return:
    """
    return True if login in clients and clients[login] == password else False


def is_client_true(login: str, _conn: socket, datetime_for_send: str):
    """ Действия при наличии клиента

    :param login:
    :return:
    """
    data_for_send = f"{datetime_for_send} -- пользователь {login} произведен вход"
    _conn.send(data_for_send.encode())


def is_client_false(login: str, _conn: socket, datetime_for_send: str):
    """ Действия при наличии клиента

    :param login:
    :return:
    """
    data_for_send = f"{datetime_for_send} -- пользователь {login} неверный пароль/логин"
    _conn.send(data_for_send.encode())

def choice_response_method(data_awnswer: str, _conn: socket):
    """ Выбор метода ответа

    :param data_awnswer: данные от клиента
    :return:
    """
    print(f"Данные от клиента: {data_awnswer}")
    _method, _path, _ver = parse_answer(data_awnswer)
    if "?" in _path:
        # узнаем есть ли параметры
        path, params = _path.split("?", 1)
    _date_time = datetime.now()
    datetime_for_send = f"{_date_time.date()} {_date_time.time().strftime("%H:%M:%S")}"
    if _ver and "HTTP" in _ver:
        if _path == "/":
            send_file_to_brower(r"html\main2.html", _conn)
        elif "/test/" in _path:
            data_for_send = _path.split("/")[2]
            send_text_to_brower(data_for_send, _conn)
        elif "message/" in _path and _path.count("/") in [3, 4]:
            _, _, login, text = _path.split("/")
            data_for_send = f"{datetime_for_send} -- сообщение от пользователя {login} -- {text}"
            print(data_for_send)
            send_text_to_brower(data_for_send, _conn)
        elif is_file(_path):
            send_file_to_brower(_path[1:].replace("/", "\\"), _conn)
        else:
            data_for_send = f"пришли неизвестные  данные по HTTP - путь {_path}"
            send_text_to_brower(data_for_send, _conn)
    elif all(param in _path for param in ["login:", "password:"]):
        _list = list(map(lambda _str: _str.split(":")[1], _path.split(";")))
        _command, _login, _password = _list[0], _list[1], _list[2]
        if _command == "reg":
            print("РЕГИСТРАЦИЯ")
            correct_login_pass(_login, _password, _conn, datetime_for_send) if check_login_and_password(_login, _password) else incorrect_login_pass(_login, _conn, datetime_for_send)
        elif _command == "signin":
            print("АВТОРИЗАЦИЯ")
            is_client_true(_login, _conn, datetime_for_send) if is_client(_login, _password) else is_client_false(
                _login, _conn, datetime_for_send)
        else:
            _conn.send(f"пришли неизвестные  данные - {_path}".encode())
    else:
        conn.send(ERR_404)


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.bind(HOST)
sock.listen()
print("-----start server-----")


try:
    while True:
        print("\n-----listen-----")
        conn, addr = sock.accept()
        data = conn.recv(1024).decode()
        if conn:
            choice_response_method(data, conn)
            # print(data)
            #send_file(r"html\main2.html", conn)
            print("-----end server-----")   # будет отрабатывать этот после каждого запроса
            conn.close()
finally:
    if conn:
        print("-----end server-----") # отработает при отключении пользователя
        conn.close()


