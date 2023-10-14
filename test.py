from http_proxy import port as proxy_port
from http import client as http_client
import ssl
import create_ca

proxy_host = '127.0.0.1'


ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
ctx.load_verify_locations(create_ca.ca_file_name)


def test(host, path="/", body=True):

    c = http_client.HTTPSConnection(proxy_host, proxy_port, context=ctx)

    c.set_tunnel(host)
    c.request('GET', path)
    r = c.getresponse()

    print(r.reason)
    if body:
        print(r.read())

    c.close()


test("api.bigdatacloud.net", '/data/client-ip')
test("ifconfig.me")
test('www.google.com', body=False)
