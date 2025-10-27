from dataclasses import dataclass


@dataclass
class AuditEvent:
    user: str
    role: str
    action: str
    id_object: int | str = "-"
    description: str = ""
