import argparse
import ssl
import socket

from datetime import datetime, UTC

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

def imprimir_campo(rotulo, valor="", largura=28, indent=0,fill="."):
    """
    Função de apresentação.
    Imprime os campos de forma organizada:
        Chave, Valor, Largura de preenchimento(default=28), indentação(opcional), char preenchimento (opcional).
    """

    espacos = " " * indent
    print(f"{espacos}{rotulo:{fill}<{largura}}: {valor}")

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
    imprimir_campo("Host", f"{args.host}:{args.port}")
    imprimir_campo("Emitido para", emitido_para)
    imprimir_campo("Emitido por", emitido_por)
    imprimir_campo("Subject Alternative Names","")
    for tipo, valor in cert["subjectAltName"]:
        imprimir_campo(tipo,valor,24,4,"_")
    imprimir_campo("Expira em",data_expiracao_local)
    imprimir_campo("Dias restantes",dias_restantes)
    imprimir_campo("Status",status)
    print("=" * 100)

if __name__ == "__main__":
    main()