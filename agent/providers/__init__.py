import os
from agent.providers.base import ProveedorWhatsApp
def obtener_proveedor():
    p = os.getenv("WHATSAPP_PROVIDER","whapi").lower()
    if p=="whapi":
        from agent.providers.whapi import ProveedorWhapi; return ProveedorWhapi()
    raise ValueError(f"Proveedor no soportado: {p}")