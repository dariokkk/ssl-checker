from dataclasses import dataclass

@dataclass
class Target:
    host: str
    port: int = 443

def carregar_hosts(arquivo):
    targets = []
    with open(arquivo, "r", encoding="utf-8") as f:
        for linha in f:
            linha = linha.strip()
            if not linha:
                continue
            if linha.startswith("#"):
                continue
            campos = linha.split(",")
            host = campos[0].strip()
            if len(campos) > 1:
                port = int(campos[1].strip())
            else:
                port = 443
            targets.append(
                Target(
                    host=host,
                    port=port
                )
        )
    return targets
