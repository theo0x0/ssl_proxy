import os
from create_ca import one_day, ten_years
from cryptography.hazmat.primitives.serialization import load_pem_private_key
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes
import datetime
from cryptography.hazmat.primitives.serialization import Encoding, PrivateFormat, NoEncryption
import create_ca

chains_dir = "certs"


def remove_cert_chains():
    try:
        os.removedirs(chains_dir)
    except:
        os.mkdir(chains_dir)


# Puts the cert chain into a file for that domain
def new_cert_chain(domain):

    # if cert already exists (doesn't check the right CA)
    try:
        open("./{}/{}".format(chains_dir, domain))
        return
    except:
        pass

    new_cert, priv = new_end_cert(domain)
    new_cert_enc = new_cert.public_bytes(Encoding.PEM).decode()
    ca = open(create_ca.ca_file_name).read()
    priv = priv.private_bytes(
        Encoding.PEM, PrivateFormat.TraditionalOpenSSL, NoEncryption()).decode()

    with open("./{}/{}".format(chains_dir, domain), "w") as f:
        f.write(priv + new_cert_enc + ca)


# Creates and signs new cert with CA
def new_end_cert(domain: str) -> tuple[x509.Certificate, ec.EllipticCurvePrivateKey]:
    ca_private_key = load_pem_private_key(
        open(create_ca.ca_key_file_name, "br").read(), None)

    private_key = ec.generate_private_key(ec.SECP256R1)
    public_key = private_key.public_key()

    builder = x509.CertificateBuilder()
    builder = builder.public_key(public_key)

    builder = builder.not_valid_before(datetime.datetime.today() - one_day)
    builder = builder.serial_number(x509.random_serial_number())
    builder = builder.not_valid_after(datetime.datetime.today() + ten_years)

    builder = builder.subject_name(
        x509.Name([
            x509.NameAttribute(NameOID.COMMON_NAME, u'SSL proxy')
        ]))
    builder = builder.issuer_name(x509.Name([
        x509.NameAttribute(NameOID.COMMON_NAME, u'SSL proxy')
    ]))

    builder = builder.add_extension(
        x509.BasicConstraints(ca=False, path_length=None), critical=True,
    )
    builder = builder.add_extension(
        x509.AuthorityKeyIdentifier.from_issuer_public_key(ca_private_key.public_key()), critical=False,
    )

    builder = builder.add_extension(
        x509.SubjectAlternativeName([x509.DNSName(domain)]), critical=False,
    )

    builder = builder.add_extension(
        x509.SubjectKeyIdentifier.from_public_key(public_key), critical=False,
    )

    certificate = builder.sign(
        private_key=ca_private_key, algorithm=hashes.SHA256())

    return certificate, private_key
