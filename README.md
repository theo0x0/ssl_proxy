# SSL proxy
Proxying all SSL traffic through a local proxy

Makes possible to customize outgoing connection

Alternatives: [Mitm](https://mitmproxy.org/), [PowerTunnel](https://github.com/krlvm/PowerTunnel)


## Requirements
`pip install h2 httpx dnspython`

## How to use
Known bugs: 
- Firefox browers doesn't allow custom certificates for domains like google.com
- Todo: http connections doesn't work

 1. Download and start http_proxy.py
    - Proxy port is 8881 by default
  
 2. Configure your network client to use HTTP proxy and the CA from `cert.pem`
    - Run test.py to check if everithing is ok

