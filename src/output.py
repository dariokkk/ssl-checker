def imprimir_campo(rotulo, valor="", largura=28, indent=0,fill="."):
    """
    Função de apresentação.
    Imprime os campos de forma organizada:
        Chave, Valor, Largura de preenchimento(default=28), indentação(opcional), char preenchimento (opcional).
    """

    espacos = " " * indent
    print(f"{espacos}{rotulo:{fill}<{largura}}: {valor}")

def imprimir_saida(host, port, emitido_para, emitido_por, sans, data_expiracao_local,dias_restantes,status):
    """
    Imprime as informações do certificado avaliado
    """
    
    print("=" * 100)
    imprimir_campo("Host", f"{host}:{port}")
    imprimir_campo("Emitido para", emitido_para)
    imprimir_campo("Emitido por", emitido_por)
    imprimir_campo("Subject Alternative Names","")
    for tipo, valor in sans:
        imprimir_campo(tipo,valor,24,4,"_")
    imprimir_campo("Expira em",data_expiracao_local)
    imprimir_campo("Dias restantes",dias_restantes)
    imprimir_campo("Status",status)
    print("=" * 100)