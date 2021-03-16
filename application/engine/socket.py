import asyncio
import datetime
import random
import websockets

from tornado.platform.asyncio import AnyThreadEventLoopPolicy

# https://github.com/tornadoweb/tornado/issues/2531
asyncio.set_event_loop_policy(AnyThreadEventLoopPolicy())

class websocketserver():
    def __init__(self, port):
        super().__init__()
        self.port = port

    async def time(self, websocket, path):
        while True:
            now = datetime.datetime.utcnow().isoformat() + "Z"
            await websocket.send(now)
            await asyncio.sleep(random.random() * 3)

    def initialize(self):
        self.server = websockets.serve(self.time, "127.0.0.1", self.port)

        asyncio.get_event_loop().run_until_complete(self.server)
        asyncio.get_event_loop().run_forever()


if __name__ == '__main__':
    socketserver = websocketserver(5678)
    socketserver.initialize()
