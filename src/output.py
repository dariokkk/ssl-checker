from certificate_info import CertificateInfo

def imprimir_campo(rotulo, valor="", largura=28, indent=0,fill="."):
    """
    Função de apresentação.
    Imprime os campos de forma organizada:
        Chave, Valor, Largura de preenchimento(default=28), indentação(opcional), char preenchimento (opcional).
    """

    espacos = " " * indent
    print(f"{espacos}{rotulo:{fill}<{largura}}: {valor}")

def imprimir_certificado(info: CertificateInfo):
    """
    Imprime as informações do certificado avaliado
    """
    print("=" * 100)
    imprimir_campo("Host", f"{info.host}:{info.port}")
    imprimir_campo("Emitido para", info.common_name)
    imprimir_campo("Emitido por", info.issuer)
    imprimir_campo("Subject Alternative Names","")
    for chave, valor in info.sans:
        imprimir_campo(chave,valor,24,4,"_")
    imprimir_campo("Expira em", info.expiration)
    imprimir_campo("Dias restantes", info.days_remaining)
    imprimir_campo("Status", info.status)
    print("=" * 100)