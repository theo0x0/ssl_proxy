import socket
import ssl
import httpx
import dns.message
import dns.query
import dns.rdatatype

def new_connect(domain, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    ip = ""

    with httpx.Client() as client:
        msg = dns.message.make_query(domain, "A")
        res = dns.query.https(msg, "https://doh.seby.io/dns-query", session=httpx.Client())

        for answer in res.answer:
            if answer.rdtype == dns.rdatatype.A:
                ip = answer[0].address

    if port == 443:
        ctx = ssl.SSLContext()
        sock = ctx.wrap_socket(sock, server_hostname='google.com')

    sock.connect((domain, port))

    return sock
