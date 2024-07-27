import asyncio
import websockets
import json

import gymnasium as gym
import random
import PIL.Image as Image

WS_SOCKET = "wss://arcade-numeric.bnr.la:3344"



class StreamWrapper(gym.Wrapper):

    def __init__(self, env,stream_metadata={}):

        super().__init__(env)
        self.ws_address = "wss://arcade-numeric.bnr.la:3344/broadcast"
        self.stream_metadata = stream_metadata
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.websocket = None
        self.loop.run_until_complete(
            self.establish_wc_connection()
        )

        self.upload_interval = 2000
        self.step_buffer = []
        self.step_send = []
        self.random = random.Random()
        self.random.seed(None)

        if hasattr(env, "pyboy"):
            self.pyboy = env.pyboy
        else:
            raise Exception("Could not find emulator!")

    def step(self, action):

        out = self.env.step(action)
        x,y,z = self.env.get_world_pos()
        notable = self.env.get_notable()
        self.send_step_info(x,y,z,notable)

        return out
    
    def reset(self, seed=None, options=None):
        return self.env.reset(seed=seed)

    async def broadcast_ws_message(self, message):
        if self.websocket is None:
            await self.establish_wc_connection()
        if self.websocket is not None:
            try:
                await self.websocket.send(message)
            except websockets.exceptions.WebSocketException as e:
                self.websocket = None

    async def establish_wc_connection(self):
        #print("Establishing connection")
        try:
            self.websocket = await websockets.connect(self.ws_address)
        except:
            self.websocket = None

    def send_step_info(self,x,y,z,notable=""):
        self.step_buffer.append({
            "x": x,
            "y": y,
            "z": z,
            "notable": notable,
        })
        if len(self.step_buffer) >= self.upload_interval:
            self.step_send = list(self.step_buffer)
            self.step_buffer = []
            self.send_step_buffer()

    def send_step_buffer(self):
        print("sending stream of steps taken")
        self.loop.run_until_complete(
            self.broadcast_ws_message(
                    json.dumps(
                        {
                            "name": "stream",
                            "metadata": self.stream_metadata,
                            "version": 1,
                            "pos_data": list(self.step_send),
                        }
                    )
                )
            
            )
        