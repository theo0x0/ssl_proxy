import datetime
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.serialization import Encoding, PrivateFormat, NoEncryption
import cert_chain

one_day = datetime.timedelta(1, 0, 0)
ten_years = datetime.timedelta(weeks=48*10)

ca_file_name = "ca.pem"
ca_key_file_name = "key.pem"


def check_or_create_ca():
    try:
        open(ca_file_name)
        open(ca_key_file_name)
    except:
        main()


def main():
    cert_chain.remove_cert_chains()

    private_key = ec.generate_private_key(ec.SECP256R1)
    public_key = private_key.public_key()

    builder = x509.CertificateBuilder()
    builder = builder.public_key(public_key)

    builder = builder.not_valid_before(datetime.datetime.today() - one_day)
    builder = builder.serial_number(x509.random_serial_number())
    builder = builder.not_valid_after(datetime.datetime.today() + ten_years)

    # subject_name and issuer_name must be the same
    builder = builder.subject_name(
        x509.Name([
            x509.NameAttribute(NameOID.COMMON_NAME, u'SSL proxy')
        ]))
    builder = builder.issuer_name(x509.Name([
        x509.NameAttribute(NameOID.COMMON_NAME, u'SSL proxy')
    ]))

    builder = builder.add_extension(
        x509.BasicConstraints(ca=True, path_length=None), critical=True,
    )
    builder = builder.add_extension(
        x509.AuthorityKeyIdentifier.from_issuer_public_key(public_key), critical=False,
    )

    builder = builder.add_extension(
        x509.SubjectKeyIdentifier.from_public_key(public_key), critical=False,
    )

    certificate = builder.sign(
        private_key=private_key, algorithm=hashes.SHA256())

    with open(ca_file_name, "w") as f:
        f.write(certificate.public_bytes(Encoding.PEM).decode())

    with open(ca_key_file_name, "w") as f:
        f.write(private_key.private_bytes(Encoding.PEM,
                PrivateFormat.TraditionalOpenSSL, NoEncryption()).decode())


if __name__ == "__main__":
    main()
