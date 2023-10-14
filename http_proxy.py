import socket
import threading
import ssl_local_server
import create_ca

port = 8881


def main():
    create_ca.check_or_create_ca()

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(('127.0.0.1', port))
    server.listen(10)

    print('Running on', port)

    while True:
        conn, _ = server.accept()
        data = conn.recv(8192)

        first_line = data.split(b"\n")[0]
        try:
            target = first_line.split()[1]
        except Exception as e:
            print("ERROR", e)
            continue

        host, _ = target.split(b":")

        conn.send(b'HTTP/1.1 200 OK\n\n')

        threading.Thread(target=ssl_local_server.new_conn,
                         args=(conn, host.decode(),)).start()


if __name__ == "__main__":
    main()
