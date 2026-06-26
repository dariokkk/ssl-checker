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

def obter_campo(campo, nome):
    """
    Extrai um atributo do subject ou issuer do certificado.
    """

    for item in campo:
        for chave, valor in item:
            if chave == nome:
                return valor

    return "N/D"

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
    emitido_para = obter_campo(cert["subject"], "commonName")
    emitido_por = obter_campo(cert["issuer"], "organizationName")

    agora_utc = datetime.now(UTC)
    agora_local = datetime.now().astimezone()
    timezone_local = agora_local.tzinfo

    data_expiracao_utc = datetime.strptime(
        cert["notAfter"],
        "%b %d %H:%M:%S %Y %Z"
    ).replace(tzinfo=UTC)
    data_expiracao_local = data_expiracao_utc.astimezone(timezone_local)

    dias_restantes = (data_expiracao_utc - agora_utc).days
    if dias_restantes < 0:
        status = "EXPIRADO"
    elif dias_restantes <= 30:
        status = "ALERTA"
    else:
        status = "OK"
    print("=" * 100)
    print(f"{'Host':.<30}: {args.host}:{args.port}")
    print(f"{'Emitido para':.<30}: {emitido_para}")
    print(f"{'Emitido por':.<30}: {emitido_por}")
    print(f"{'Subject Alternative Names':.<30}:")
    for tipo, valor in cert["subjectAltName"]:
        print(f"{'': <4}{tipo:<26}: {valor}") 
    print(f"{'Expira em':.<30}: {data_expiracao_local}")
    print(f"{'Dias restantes':.<30}: {dias_restantes}")
    print(f"{'Status':.<30}: {status}")
    print("=" * 100)

if __name__ == "__main__":
    main()