import os, logging, httpx
from fastapi import Request
from agent.providers.base import ProveedorWhatsApp, MensajeEntrante
logger = logging.getLogger("agentkit")
class ProveedorWhapi(ProveedorWhatsApp):
    def __init__(self):
        self.token = os.getenv("WHAPI_TOKEN")
        self.url_envio = "https://gate.whapi.cloud/messages/text"
    async def parsear_webhook(self, request: Request):
        try: body = await request.json()
        except: return []
        msgs = []
        for msg in body.get("messages",[]):
            if msg.get("type") != "text": continue
            msgs.append(MensajeEntrante(telefono=msg.get("chat_id",""),texto=msg.get("text",{}).get("body",""),mensaje_id=msg.get("id",""),es_propio=msg.get("from_me",False)))
        return msgs
    async def enviar_mensaje(self, telefono, mensaje):
        if not self.token: return False
        try:
            async with httpx.AsyncClient(timeout=15.0) as c:
                r = await c.post(self.url_envio, json={"to":telefono,"body":mensaje}, headers={"Authorization":f"Bearer {self.token}","Content-Type":"application/json"})
                return r.status_code == 200
        except: return False