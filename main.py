import socket

def send_hello_world():
    server_ip = '192.168.0.176'
    server_port = 97

    # Создаем TCP/IP сокет
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Соединяемся с сервером
        sock.connect((server_ip, server_port))

        # Отправляем данные
        message = 'hello world'
        print(f"Отправка: {message}")
        sock.sendall(message.encode('utf-8'))

        # Ждем ответа сервера (эхо)
        response = sock.recv(1024)
        print(f"Получен ответ: {response.decode('utf-8')}")
    finally:
        # Закрываем соединение
        sock.close()


send_hello_world()
