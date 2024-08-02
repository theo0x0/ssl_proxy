import socket
import threading
import ssl_local_server
import create_ca
from urllib.parse import urlparse
import ssl

port = 8881


def main():
    create_ca.check_or_create_ca()

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(('127.0.0.1', port))
    server.listen()

    print('Running on', port)

    while True:
        conn, _ = server.accept()
        params = conn.recv(8192).decode().split(" ")

        target = params[1]

        if params[0] != "CONNECT":
            conn.close()
            continue

        host, target_port = target.split(":")

        conn.send(b'HTTP/1.1 200 OK\n\n')

        threading.Thread(target=ssl_local_server.new_conn,
                         args=(conn, host, int(target_port),)).start()



if __name__ == "__main__":
    main()
