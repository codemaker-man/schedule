from subprocess import Popen, PIPE
from utils import getlogger
from .config import LOG_PATH

logger = getlogger(__name__, LOG_PATH)

from .msg import Message
class Executor:


    def run(self, script, timeout=True):
        logger.info('Agent start ~~~~')
        proc = Popen(script, shell=True, stdout=PIPE)
        code = proc.wait()
        output = proc.stdout.read()
        logger.info(code)
        logger.info(output)
        return code, output
