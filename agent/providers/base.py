from abc import ABC, abstractmethod
from dataclasses import dataclass
from fastapi import Request
@dataclass
class MensajeEntrante:
    telefono: str; texto: str; mensaje_id: str; es_propio: bool
class ProveedorWhatsApp(ABC):
    @abstractmethod
    async def parsear_webhook(self, request): ...
    @abstractmethod
    async def enviar_mensaje(self, telefono, mensaje): ...
    async def validar_webhook(self, request): return None