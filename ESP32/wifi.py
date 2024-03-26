import machine
import socket
import time
from blink import blink_led

retry_pause = 1.0
led = machine.Pin(2, machine.Pin.OUT)
led.value(False)

def do_connect():
    import network
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        led.value(False)
        print('connecting to network...')
        wlan.connect('AsusHome', '89117788551')
        while not wlan.isconnected():
            time.sleep(retry_pause)
            pass
    led.value(True)
    print('network config:', wlan.ifconfig())
    
def listen_on_port_97(lcd):
    host = '0.0.0.0'  # Привязка ко всем доступным сетевым интерфейсам
    port = 97

    # Создаем TCP сокет
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Привязываем сокет к указанному хосту и порту
    sock.bind((host, port))

    # Начинаем прослушивание порта с указанием количества возможных непринятых соединений
    sock.listen(1)
    print("Сервер слушает порт {}".format(port))

    try:
        while True:
            # Принимаем входящее соединение
            conn, addr = sock.accept()
            print("Подключение от {}".format(addr))

            # Получаем данные от клиента
            data = conn.recv(1024)
            if data:
                request = data.decode('utf-8')
                print(f'Получены данные: {request}')
                
                headers, body = request.split('\r\n\r\n', 1)
                if body:
                    lcd.putstr(body)
                    blink_led()
                    time.sleep(2)
                    lcd.clear()
                    
            # Закрываем соединение
            response = 'HTTP/1.1 200 OK\r\nAccess-Control-Allow-Origin: *\r\nContent-Type: text/plain\r\n\r\n' + 'Данные получены и обработаны.'
            conn.sendall(response.encode('utf-8'))
            conn.close()
    except KeyboardInterrupt:
        print("Сервер остановлен")
    finally:
        # Закрываем сокет
        sock.close()
        