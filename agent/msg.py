import socket, os, uuid
import netifaces  #接口信息
import ipaddress #地址验证

class Message:
    def __init__(self, myidpath):
        if os.path.exists(myidpath):
            with open(myidpath) as f:
                self.id = f.readline().strip()
        else:
            self.id = uuid.uuid4().hex  #获取uuid
            with open(myidpath, 'w') as f:
                f.write(self.id)

    def _get_address(self):
        addr = []

        for ifaces in netifaces.interfaces():
            all_address = netifaces.ifaddresses(ifaces)
            address = all_address.get(2, None)  #address-> [{'addr': '192.168.56.1', 'netmask': '255.255.255.0', 'broadcast': '192.168.56.255'}]

            if not address:   # {2：address}是目标地址
                continue

            for ip_info in address:  # 一个网卡上可能有多个地址 {'addr': '192.168.56.1', 'netmask': '255.255.255.0',...}
                target = ip_info['addr']   # str
                ip = ipaddress.ip_address(ip_info['addr'] )# 192.168.56.1 -><class 'ipaddress.IPv4Address'>
                if ip.version != 4:  #去除不想要的ip地址
                    continue
                if ip.is_link_local:
                    continue
                if ip.is_multicast:
                    continue
                if ip.is_reserved:
                    continue
                if ip.is_loopback:
                    continue
                addr.append(target)
        return addr

    @property
    def reg(self):
        return {
            'type':'register',
            'payload':{
                'id': self.id,
                'hostname': socket.gethostname(),
                'ip':self._get_address()
            }
        }

    @property
    def heartbeat(self):
        return {
            'type' : 'heartbeat',
            'payload' : {
                'id':self.id,
                'hostname': socket.gethostname(),
                'ip':self._get_address()
            }
        }


    def result(self, task_id, code, output):
        return {
            'type': 'result',
            'payload': {
                'id': task_id,
                'agent_id':self.id,
                'code':code,
                'output':output
            }
        }