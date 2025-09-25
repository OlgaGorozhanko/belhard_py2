import re


clients = {"test1": {"fio": "TEST1", "password": "passTEST1", "age": 8, "email": "test1@gmail.com"}}


def is_client(login: str, password: str) -> bool:
    """ Проверка наличие клиента в базе

    :param login:
    :param password:
    :return:
    """
    print(f"is_client({login}, {password}) -- {True if clients[login]["password"] == password else False}")
    return True if clients[login]["password"] == password else False


def __check_fio(fio: str) -> bool:
    """ Проверка корректности ФИО

    :param fio:
    :return:
    """
    print(f"__check_fio({fio}) -- {bool(re.fullmatch(r'[А-я\s]+', fio))}")
    return True if bool(re.fullmatch(r'[А-я\s]+', fio)) else "error_fio"


def __check_login(login: str) -> bool | str:
    """ Проверка на корректность логина

    :param login:
    :return:
    """
    print(f"__check_login({login}) -- {True if login.isalnum() and 6 <= len(login) <= 20 else False}")
    if login in clients:
        return "Логин занят"
    return True if login.isalnum() and 6 <= len(login) <= 20 else "error_login"


def __check_password(password: str) -> bool:
    templ = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[A-Za-z\d]{8,15}$'
    print(f"__check_password({password}) -- {bool(re.match(templ, password))}")
    return True if bool(re.match(templ, password)) else "error_pass"


def __check_email(email: str) -> bool:
    templ = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    print(f"__check_email({email}) -- {bool(re.match(templ, email))}")
    return True if bool(re.match(templ, email)) else "error_email"


def __check_age(age: str) -> bool|str:
    print(f"__check_age({age}) -- {True if 12 <= int(age) <= 100 else False}")
    return True if 12 <= int(age) <= 100 else "error_age"


def check_valid(fio: str, login: str, password: str, email: str, age: str) -> bool | list[str]:
    """  Проверка валидности всех полей

    :param fio:
    :param login:
    :param password:
    :param email:
    :param age:
    :return: True если все данные валидны, иначе False
    """
    print("check_valid")
    error_group = [elem for elem in [__check_fio(fio), __check_login(login),  __check_password(password), __check_age(age), __check_email(email)] if elem  != True]
    return error_group if error_group else True


def add_client(fio: str, login: str, password: str, email: str, age: str) -> bool:
    global clients
    try:
        clients[login] = {"fio": fio, "password": password, "age": age, "email": email}
        print(clients)
        return True
    except:
        return False

