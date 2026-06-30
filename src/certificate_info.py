from dataclasses import dataclass
from datetime import datetime

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