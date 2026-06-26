import argparse
import ssl
import socket

from datetime import datetime, UTC

port = 443

def consultar_certificado(host, port):
    """
    Consulta o certificado SSL/TLS de um host remoto.

    Argumentos:
        host: Nome do host.
        port: Porta TCP.

    Returns:
        dict contendo o certificado.
    """
    contexto = ssl.create_default_context()

    with contexto.wrap_socket(
        socket.socket(),
        server_hostname=host
    ) as conexao:

        conexao.settimeout(5)
        conexao.connect((host, port))

        return conexao.getpeercert()


def main():
    """
    Função principal.

    Obtem parâmetros (URL e Porta)

    Exibe data de expiração e de dias restantes de validade do certificado.
        
    """
    parser = argparse.ArgumentParser(
        description="Verificador de certificados SSL/TLS"
    )
    parser.add_argument(
        "--host",
        help="Host a ser consultado"
    )
    parser.add_argument(
        "--port",
        type=int,
        default=443,
        help="Porta TCP (default:443)"
    )
    args = parser.parse_args()

    mensagem_erro = "Falha ao verificar o certificado!"
    try:
        cert = consultar_certificado(
            args.host,
            args.port
            )
    except socket.gaierror:
        print(mensagem_erro)
        print("Host não encontrado.")
        return

    except TimeoutError:
        print(mensagem_erro)
        print("Timeout.")
        return

    except ssl.SSLError as e:
        print(mensagem_erro)
        print(e)
        return

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