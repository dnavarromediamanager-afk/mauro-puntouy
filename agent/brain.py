import os, yaml, logging
from anthropic import AsyncAnthropic
from dotenv import load_dotenv
load_dotenv()
logger = logging.getLogger("agentkit")
client = AsyncAnthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
def cargar_system_prompt():
    try:
        with open("config/prompts.yaml","r",encoding="utf-8") as f:
            return yaml.safe_load(f).get("system_prompt","Sos Mauro de PuntoUY.")
    except: return "Sos Mauro de PuntoUY Comunicaciones. Responde en espanol rioplatense."
async def generar_respuesta(mensaje, historial):
    if not mensaje or len(mensaje.strip()) < 2: return "Disculpa, no entendi. Podes reformularlo?"
    mensajes = [{"role":m["role"],"content":m["content"]} for m in historial]
    mensajes.append({"role":"user","content":mensaje})
    try:
        r = await client.messages.create(model="claude-sonnet-4-6",max_tokens=1024,system=cargar_system_prompt(),messages=mensajes)
        return r.content[0].text
    except Exception as e:
        logger.error(f"Error Claude: {e}"); return "Tuve un problema tecnico. Me podes reenviar?"