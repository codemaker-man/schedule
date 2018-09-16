from .agent import Agent
import datetime
from .task import Task
from .state import *

# { agent
#             'type':'reg',
#             'payload':{
#                 'id': self.id,
#                 'hostname': socket.gethostname(),
#                 'ip':self._get_address()
#             }
#         }


class Storage:
    def __init__(self):
        self.agents = {}
        self.tasks = {}

    def reg_hb(self, id, info):
        self.agents[id] = {
            'heartbeat':datetime.datetime.now(),
            'info':info,
            'busy':self.agents.get(id, {}).get('busy', False) #todo
        }

    def add_task(self, task:dict):
        t = Task(**task)
        self.tasks[t.id] = t
        return t.id

    def iter_tasks(self, states={WATTING, RUNNING}):
        yield from (task for task in self.tasks.values()
                    if task.state in states)

    def get_task_by_agentid(self, agent_id, state=WATTING):
        for task in self.iter_tasks():
            if agent_id in task.targets.keys():
                t = task.targets.get(id)
                if t.get('state') == state:
                    return task, t

    def get_task_by_id(self, task_id)->Task:
        return self.tasks.get(task_id)

    def get_agents(self):
        return list(self.agents.keys())
