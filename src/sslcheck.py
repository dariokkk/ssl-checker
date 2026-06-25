import ssl
import socket

from datetime import datetime


host = "google.com"
port = 443

ctx = ssl.create_default_context()

with ctx.wrap_socket(
    socket.socket(),
    server_hostname=host
) as conn:

    conn.settimeout(5)
    conn.connect((host, port))

    cert = conn.getpeercert()

data_expiracao = datetime.strptime(
    cert["notAfter"],
    "%b %d %H:%M:%S %Y %Z"
)
#agora_utc = datetime.now(timezone.utc)

dias_restantes = (data_expiracao - datetime.utcnow()).days

print(f"Host: {host}")
print(f"Expira em: {data_expiracao}")
print(f"Dias restantes: {dias_restantes}")
