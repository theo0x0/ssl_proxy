from socket import socket
import ssl
import ssl_remote_connect
import cert_chain as cert_chain
import threading


def new_conn(conn: socket, host, port):

    ctx = ssl.SSLContext()
    cert_chain.new_cert_chain(host)
    ctx.load_cert_chain("./certs/" + host)

    conn = ctx.wrap_socket(conn, True)

    remote_conn = ssl_remote_connect.new_connect(host, port)

    # connects two sockets
    def pipe(conn1: ssl.SSLSocket, conn2: ssl.SSLSocket):
        while True:
            try:
                conn1.send(conn2.recv(12000))
            except Exception as e:
                conn1.close()
                conn2.close()
                print(e)
                break

    threading.Thread(target=pipe, args=(conn, remote_conn)).start()
    threading.Thread(target=pipe, args=(remote_conn, conn)).start()
