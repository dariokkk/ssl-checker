import argparse
import ssl
import socket

from datetime import datetime, UTC

port = 443

def consultar_certificado(host, port=443):

    contexto = ssl.create_default_context()

    with contexto.wrap_socket(
        socket.socket(),
        server_hostname=host
    ) as conexao:

        conexao.settimeout(5)
        conexao.connect((host, port))

        return conexao.getpeercert()


def main():
    parser = argparse.ArgumentParser(
        description="Verificador de certificados SSL/TLS"
    )
    parser.add_argument(
        "host",
        help="Host a ser consultado"
    )
    args = parser.parse_args()
    cert = consultar_certificado(args.host)

    agora_utc = datetime.now(UTC)
    agora_local = datetime.now().astimezone()
    timezone_local = agora_local.tzinfo

    data_expiracao_utc = datetime.strptime(
        cert["notAfter"],
        "%b %d %H:%M:%S %Y %Z"
    ).replace(tzinfo=UTC)
    data_expiracao_local = data_expiracao_utc.astimezone(timezone_local)

    dias_restantes = (data_expiracao_utc - agora_utc).days

    print(f"Host............: {args.host}")
    print(f"Expira em.......: {data_expiracao_local}")
    print(f"Dias restantes..: {dias_restantes}")

if __name__ == "__main__":
    main()