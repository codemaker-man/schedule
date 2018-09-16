import zerorpc
import threading

from .msg import Message
from utils import getlogger
from .config import LOG_PATH
from .state import *
from .executor import Executor

logger = getlogger('__name__', LOG_PATH)

class Agentclient:
    def __init__(self, url, message:Message):
        self.message = message
        self.client = zerorpc.Client()
        self.event = threading.Event()
        self.url = url
        self.state = WATTING  #标记任务是否完成
        self.executor = Executor()

    def start(self, itime=3):
        try:  # 记录异常日志

            self.event.clear()
            self.client.connect(self.url)
            reg = self.client.message(self.message.reg)
            print('reg: ', reg)
            logger.info(reg)
            while not self.event.wait(itime):
                server_message = self.client.message(self.message.heartbeat)
                print('hb: ~~~~~')
                if self.state == WATTING:
                    self._get_task(self.message.id)

        except Exception as e:
            print('client start error: ', e)
            logger.info('Fail to connect to master. Reason:{}'.format(e))
            raise e

    def stop(self):
        self.event.set()
        self.client.close()


    def _get_task(self, agent_id):
        task = self.client.take_task(self.message.id)
        if task:
            logger.info('{}'.format(task))
            self.state = RUNNING
            script = task['script']
            code, output = self.executor.run(script)
            self.client.message(self.message.result(task['id'], code, output))
            self.state = WATTING




