import argparse
import socket
import ssl
import sys

from datetime import datetime, UTC
from certificate_info import CertificateInfo
import output
import certificate

def main():
    """
    Função principal.
    Obtem parâmetros (URL e Porta)
    Exibe data de expiração e de dias restantes de validade do certificado.
    """

    parser = argparse.ArgumentParser(
        description="Verificador de certificados SSL/TLS"
    )
    if len(sys.argv) == 1:
        parser.print_help()
        return
    parser.add_argument(
        "host",
        help="Host a ser consultado."
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
        cert = certificate.consultar_certificado(
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
    emitido_para = certificate.obter_campo(cert["subject"], "commonName")
    emitido_por = certificate.obter_campo(cert["issuer"], "organizationName")

    agora_utc = datetime.now(UTC)
    timezone_local = datetime.now().astimezone().tzinfo

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
    
    info = CertificateInfo(
        host=args.host,
        port=args.port,
        common_name=emitido_para,
        issuer=emitido_por,
        expiration=data_expiracao_local,
        days_remaining=dias_restantes,
        status=status,
        sans=cert["subjectAltName"]
    )
    output.imprimir_certificado(info)

if __name__ == "__main__":
    main()