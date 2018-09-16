
import aiohttp
from aiohttp import web, log
import zerorpc

client = zerorpc.Client()
client.connect('tcp://127.0.0.1:9999')

async def targetshandler(request:web.Request):
    txt = client.get_agents()
    return web.json_agents(txt)

async def taskhandler(requset:web.Request):
    j = await requset.json()
    txt = client.add_task(j)
    return web.Response(text=txt, status=201)
app = web.Application()
app.router.add_get('/task/targets', targetshandler)

web.run_app(app, host='0.0.0.0', port=8080)