import socket


HOST = ("127.0.0.1", 7777)


def compose_welcome_message(name: str) -> str:
    return f"\nПриветствую {name}! Приятно познакомиться)\nДавай вместе изучать фрэймворки Python)\n"


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.bind(HOST)
sock.listen()
print("--start server--")

conn = None
try:
    while True:
        conn, addr = sock.accept()
        data_name_client = conn.recv(1024).decode()
        data_return = compose_welcome_message(data_name_client)
        conn.send(data_return.encode())
finally:
    if conn:
        print("--end server--")
        conn.close()


