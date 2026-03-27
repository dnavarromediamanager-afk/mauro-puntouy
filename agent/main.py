import os, logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import PlainTextResponse
from dotenv import load_dotenv
from agent.brain import generar_respuesta
from agent.memory import inicializar_db, guardar_mensaje, obtener_historial
from agent.providers import obtener_proveedor
load_dotenv()
logging.basicConfig(level=logging.INFO,format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("agentkit")
proveedor = obtener_proveedor()
@asynccontextmanager
async def lifespan(app):
    await inicializar_db(); logger.info("Mauro iniciado - PuntoUY"); yield
app = FastAPI(title="Mauro - PuntoUY", lifespan=lifespan)
@app.get("/")
async def health(): return {"status":"ok","agente":"Mauro","negocio":"PuntoUY Comunicaciones"}
@app.get("/webhook")
async def wh_get(request: Request):
    r = await proveedor.validar_webhook(request)
    if r is not None: return PlainTextResponse(str(r))
    return {"status":"ok"}
@app.post("/webhook")
async def wh_post(request: Request):
    try:
        msgs = await proveedor.parsear_webhook(request)
        for msg in msgs:
            if msg.es_propio or not msg.texto.strip(): continue
            h = await obtener_historial(msg.telefono)
            resp = await generar_respuesta(msg.texto, h)
            await guardar_mensaje(msg.telefono,"user",msg.texto)
            await guardar_mensaje(msg.telefono,"assistant",resp)
            await proveedor.enviar_mensaje(msg.telefono, resp)
        return {"status":"ok"}
    except Exception as e: raise HTTPException(status_code=500,detail=str(e))