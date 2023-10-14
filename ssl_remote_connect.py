import socket
import ssl


def new_connect(domain):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Custom nameserver usage
    try:
        from dns import resolver

        dns = resolver.Resolver()
        # dns.nameservers = ["127.0.0.1"]
        # dns.nameserver_ports = {"127.0.0.1": 5332}

        domain = dns.resolve(domain, 'A')[0].address
    except:
        pass

    ctx = ssl.SSLContext()
    sock = ctx.wrap_socket(sock)

    sock.connect((domain, 443))

    return sock
