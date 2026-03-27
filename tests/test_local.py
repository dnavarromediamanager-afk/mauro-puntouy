import asyncio, sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from agent.brain import generar_respuesta
from agent.memory import inicializar_db, guardar_mensaje, obtener_historial, limpiar_historial
TELEFONO = "test-001"
async def main():
    await inicializar_db()
    print("="*50); print("   MAURO - Agente PuntoUY"); print("   limpiar | salir"); print("="*50)
    while True:
        try: msg = input("Vos: ").strip()
        except (EOFError, KeyboardInterrupt): break
        if not msg: continue
        if msg.lower()=="salir": break
        if msg.lower()=="limpiar": await limpiar_historial(TELEFONO); print("[Historial borrado]"); continue
        h = await obtener_historial(TELEFONO)
        print("Mauro: ", end="", flush=True)
        r = await generar_respuesta(msg, h); print(r+"\n")
        await guardar_mensaje(TELEFONO,"user",msg); await guardar_mensaje(TELEFONO,"assistant",r)
if __name__ == "__main__": asyncio.run(main())