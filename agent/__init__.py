
from .client import Agentclient
from .msg import Message
from .config import MASTER_URL, ID_PATH, Interval_time
import threading

class Agent:
    def __init__(self):
        self.msg = Message(ID_PATH)
        self.agentclient = Agentclient(MASTER_URL, self.msg)
        self.event = threading.Event()

    def start(self):
        while not self.event.is_set():
            try:
                self.agentclient.start(Interval_time)
            except Exception as e:
                print('Agent error:', e)
                self.agentclient.stop()
            self.event.wait(2)

    def stop(self):
        self.event.set()
        self.agentclient.stop()


