
class Agent:
    def __init__(self, **infos):
        self.ip = infos['ip']
        self.hostname = infos['hostname']

    def __repr__(self):
        return '<Agent {} {}>'.format(self.ip, self.hostname)

    __str__ = __repr__
