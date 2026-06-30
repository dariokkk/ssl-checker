# SSL Checker

Ferramenta para verificação de certificados SSL/TLS.

## Funcionalidades

- Consulta certificado remoto
- Exibe validade
- Calcula dias restantes

Exemplo de uso:
python src/sslcheck.py www.github.com --port 443

Exemplo de saída:
'====================================================================================================
Host........................: www.github.com:443
Emitido para................: github.com
Emitido por.................: Sectigo Limited
Subject Alternative Names...: 
    DNS_____________________: github.com
    DNS_____________________: www.github.com
Expira em...................: 2026-08-02 20:59:59-03:00
Dias restantes..............: 33
Status......................: OK
===================================================================================================='

## Autor

Dario Kuceki Knopfholz
