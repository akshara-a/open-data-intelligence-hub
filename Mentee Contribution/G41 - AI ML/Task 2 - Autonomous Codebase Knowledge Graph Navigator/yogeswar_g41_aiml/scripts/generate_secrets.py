import os
from pathlib import Path
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization, hashes
from cryptography import x509
from cryptography.x509.oid import NameOID
import datetime

secrets_dir = Path("secrets")
secrets_dir.mkdir(parents=True, exist_ok=True)

# 1. Generate JWT RS256 Keypair
jwt_private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
)
jwt_priv_pem = jwt_private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption(),
)
jwt_pub_pem = jwt_private_key.public_key().public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo,
)

(secrets_dir / "jwt_private_key.pem").write_bytes(jwt_priv_pem)
(secrets_dir / "jwt_public_key.pem").write_bytes(jwt_pub_pem)

# 2. Generate Internal Service RS256 Keypair
internal_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
)
internal_priv_pem = internal_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption(),
)
internal_pub_pem = internal_key.public_key().public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo,
)

(secrets_dir / "internal_service_key.pem").write_bytes(internal_priv_pem)
(secrets_dir / "internal_service_pubkey.pem").write_bytes(internal_pub_pem)

# 3. Neo4j & Admin Passwords (min 12 chars per architecture Section 19.2)
import secrets
import string

alphabet = string.ascii_letters + string.digits + "!@#$%^&*-_+="

if not (secrets_dir / "neo4j_admin.password").exists():
    neo_pwd = "".join(secrets.choice(alphabet) for _ in range(32))
    (secrets_dir / "neo4j_admin.password").write_text(f"{neo_pwd}\n", encoding="utf-8")
    (secrets_dir / "neo4j_read.password").write_text(f"{neo_pwd}\n", encoding="utf-8")
    (secrets_dir / "neo4j_write.password").write_text(f"{neo_pwd}\n", encoding="utf-8")

if not (secrets_dir / "admin.password").exists():
    admin_pwd = "".join(secrets.choice(alphabet) for _ in range(32))
    (secrets_dir / "admin.password").write_text(f"{admin_pwd}\n", encoding="utf-8")

# 4. Generate Self-Signed TLS Certs for Nginx (nginx/certs)
nginx_certs_dir = Path("nginx/certs")
nginx_certs_dir.mkdir(parents=True, exist_ok=True)

tls_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
)
subject = issuer = x509.Name([
    x509.NameAttribute(NameOID.COUNTRY_NAME, "US"),
    x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, "CA"),
    x509.NameAttribute(NameOID.LOCALITY_NAME, "San Francisco"),
    x509.NameAttribute(NameOID.ORGANIZATION_NAME, "Knowledge Graph Navigator"),
    x509.NameAttribute(NameOID.COMMON_NAME, "localhost"),
])
cert = x509.CertificateBuilder().subject_name(
    subject
).issuer_name(
    issuer
).public_key(
    tls_key.public_key()
).serial_number(
    x509.random_serial_number()
).not_valid_before(
    datetime.datetime.now(datetime.timezone.utc)
).not_valid_after(
    datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=365)
).add_extension(
    x509.SubjectAlternativeName([x509.DNSName("localhost"), x509.IPAddress(ipaddress.IPv4Address("127.0.0.1"))] if False else [x509.DNSName("localhost")]),
    critical=False,
).sign(tls_key, hashes.SHA256())

(nginx_certs_dir / "tls.key").write_bytes(
    tls_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption(),
    )
)
(nginx_certs_dir / "tls.crt").write_bytes(
    cert.public_bytes(serialization.Encoding.PEM)
)

print("Generated secrets and TLS certificates successfully.")
