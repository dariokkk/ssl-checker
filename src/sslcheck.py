import ssl
import socket

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

print(cert["notAfter"])
