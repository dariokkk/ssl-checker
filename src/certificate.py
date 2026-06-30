from dataclasses import dataclass
from datetime import datetime
import ssl
import socket

@dataclass
class CertificateInfo:
    host: str
    port: int
    common_name: str
    issuer: str
    expiration: datetime
    days_remaining: int
    status: str
    sans: list[tuple[str,str]]

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