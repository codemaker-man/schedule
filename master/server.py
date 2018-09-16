import zerorpc

from agent.config import MASTER_URL
from .storage import Storage
from utils import getlogger
from .config import LOG_PATH
from .storage import *
import uuid

logger = getlogger(__name__, LOG_PATH)


class Agentserver:
    def __init__(self):
        self.store = Storage()

    def handle(self, msg):
        logger.info(type(msg))
        try:
            if msg['type'] in {'register', 'heartbeat'}:
                print(1)
                payload = msg['payload']
                print(2)
                info = {'hostname': payload['hostname'], 'ip': payload['ip']}
                print(3)
                self.store.reg_hb(payload['id'], info)
                print(4)
                logger.info('{}'.format(self.store.agents))
                return 'ack {}'.format(msg)


            elif msg['type'] == 'result':
                payload = msg['payload']
                agent_id = payload['agent_id']
                task_id = payload['id']
                state = SUCCEED if payload['code']==0 else FAILED
                output = payload['output']

                task = self.store.get_task_by_agentid(task_id)
                t = task.targets[agent_id]
                t.state = state
                t.ouput = output
                return 'ack result'


        except Exception as e:
            logger.error(''.format(e))
            return 'Bad Request'

    message = handle

    def take_task(self, agent_id):

        info = self.store.get_task_by_agentid(agent_id)  # 去看有没有要自己执行的任务
        if info:
            task, target = info
            task.state = RUNNING
            target['state'] = RUNNING
            return {
                'id': task.id,
                'script': task.script,
                'timeout': task.timeout
            }

    def get_agents(self):
        return self.store.get_agents()

    def add_task(self, task):
        task['task_id'] = uuid.uuid4().hex
        return self.store.add_task(task)