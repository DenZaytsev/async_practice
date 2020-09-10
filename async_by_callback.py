import socket
import selectors

selector = selectors.DefaultSelector()  # отличаются у разных операционных систем метод select


def server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('localhost', 5000))  # создается файл сокета

    server_socket.listen()  # прослушивает внешний буфер на предмет входящих подключений
    selector.register(fileobj=server_socket, events=selectors.EVENT_READ, data=accept_connection)


def accept_connection(server_socket):
    client_socket, adr = server_socket.accept()
    selector.register(fileobj=client_socket, events=selectors.EVENT_READ, data=send_massage)


def send_massage(client_socket):
    request = client_socket.recv(4096)
    print(client_socket)
    if request:
        response = 'aaaaaaaaaaaa\n'.encode()
        client_socket.send(response)
    else:
        selector.unregister(client_socket)
        client_socket.close()


def event_loop():
    while True:

        events = selector.select()  # return (key, events)

        for key, _ in events:
            callback = key.data
            callback(key.fileobj)


if __name__ == "__main__":
    server()
    event_loop()
