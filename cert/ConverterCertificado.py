import os
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.serialization import Encoding, PrivateFormat, NoEncryption
from cryptography.hazmat.primitives.serialization.pkcs12 import load_key_and_certificates


def convert_pfx_to_pem(pfx_path, cert_path, key_path, pfx_password=None):
    try:
        with open(pfx_path, 'rb') as f:
            pfx_data = f.read()

        private_key, certificate, additional_certificates = load_key_and_certificates(
            pfx_data,
            pfx_password.encode() if pfx_password else None,
            default_backend()
        )

        with open(key_path, 'wb') as f:
            f.write(private_key.private_bytes(
                Encoding.PEM,
                PrivateFormat.TraditionalOpenSSL,
                NoEncryption()
            ))

        # Escrever o certificado em um arquivo PEM
        with open(cert_path, 'wb') as f:
            f.write(certificate.public_bytes(Encoding.PEM))

        print("Conversão concluída com sucesso.")
    except Exception as e:
        print(f"Erro ao converter PFX para PEM: {e}")


if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    pfx_file = r'C:\Users\raysl_3a68bgu\Downloads\cert.pfx'
    cert_file = os.path.join(current_dir, 'cert.pem')
    key_file = os.path.join(current_dir, 'key.pem')

    pfx_password = '1234'

    convert_pfx_to_pem(pfx_file, cert_file, key_file, pfx_password)
