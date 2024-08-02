import socket
import threading
import ssl_local_server
import create_ca
import ssl
import httpx
import dns.message
import dns.query
import dns.rdatatype
import copy

port = 8881


def main():

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(('127.0.0.1', port))
    server.listen()

    print('Running on', port)

    while True:
        conn, _ = server.accept()
        http_data = conn.recv(8192)

        first_line = http_data.split(b"\n")[0]
        target = first_line.split()[1]
        #print(target)

        host, traget_port = target.split(b":")

        conn.send(b'HTTP/1.1 200 OK\n\n')
        threading.Thread(target=new_conn,
                         args=(conn, host.decode(),)).start()

def new_conn(conn, host):
    data = clear_data(conn)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
   # ip = ""
   # with httpx.Client() as client:
  #      msg = dns.message.make_query(domain, "A")
  #      res = dns.query.https(msg, "https://doh.seby.io/dns-query", session=httpx.Client())
  #      for answer in res.answer:
  #          if answer.rdtype == dns.rdatatype.A:
  #              ip = answer[0].address
    


  #  ctx = ssl.SSLContext()
  #  sock = ctx.wrap_socket(sock)

    sock.connect((host, 443))
    print()
    sock.send(data)

    

    def pipe(conn1, conn2):
        while True:
            try:
             #   print(1)
                conn1.send(conn2.recv(12000))
             #   print(1)
                
            except Exception as e:
                conn1.close()
                conn2.close()
                print(e)
                break

    threading.Thread(target=pipe, args=(conn, sock)).start()
    threading.Thread(target=pipe, args=(sock, conn)).start()

def clear_data(conn):
        res = []

        res.append(conn.recv(1 + 2))

        tls_len = int.from_bytes(conn.recv(2), 'big')

        res.append(conn.recv(1))

        handshake_len = int.from_bytes(conn.recv(3), 'big')

        res.append(conn.recv(2 + 32 + 1 + 32 + 2))
        
        res.append(conn.recv(int.from_bytes(res[-1][-2:], 'big') + 2))
        
        
        ext_len = int.from_bytes(conn.recv(2), 'big')
        all_ext = b''
        
        i = 0
        hostname_len = 0

        while i < ext_len:
            ext = b''
            ext += conn.recv(2)
            type = int.from_bytes(ext[-2:], 'big')
            ext += conn.recv(2)
            data_len = int.from_bytes(ext[-2:], 'big')

            ext_data = conn.recv(data_len)
            
            if type != 0:
                all_ext += ext + ext_data
            else:
                hostname_len = data_len

            i += 4 + data_len

        
        print(i, ext_len)
       
        ext_len -= 4 + hostname_len
        handshake_len -= 4 + hostname_len
        tls_len -= 4 + hostname_len

        res.insert(1, tls_len.to_bytes(2))
        res.insert(3, handshake_len.to_bytes(3))
        res.append(ext_len.to_bytes(2) + all_ext)

        return b''.join(res)

if __name__ == "__main__":
    main()
