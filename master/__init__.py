import zerorpc
import threading
from .config import MASTER_URL
from .server import Agentserver



class Master:
    def __init__(self):
        self.server = zerorpc.Server(Agentserver())
        self.server.bind(MASTER_URL)

    def start(self):
        self.server.run()

    def stop(self):
        self.server.close()
