import socket
from select import select

# select нужна для отслеживания изменений файловых обьектов

to_monitor = []
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(('localhost', 5000))  # создается файл сокета

server_socket.listen()  # прослушивает внешний буфер на предмет входящих подключений


def accept_connection(server_socket):
    client_socket, adr = server_socket.accept()
    to_monitor.append(client_socket)


def send_massage(client_socket):
    request = client_socket.recv(4096)
    print(client_socket)
    if request:
        response = 'aaaaaaaaaaaa\n'.encode()
        client_socket.send(response)
    else:
        client_socket.close()


def event_loop():
    while True:
        ready_to_read, ready_to_write, _ = select(to_monitor, [], [])

        for sock in ready_to_read:
            accept_connection(sock) if sock is server_socket else send_massage(sock)


if __name__ == "__main__":
    to_monitor.append(server_socket)
    event_loop()
