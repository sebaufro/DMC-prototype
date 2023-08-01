import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '.'))
import signal
import Ice
from core.metasingleton import SingletonMeta


class iceSingletonServer(metaclass=SingletonMeta):
    __adapter = None
    __communicator = None
    def __init__(self):
        if self.__communicator is None:
            self.__communicator = Ice.initialize(sys.argv, "config.server")
            signal.signal(signal.SIGINT, lambda signum, frame: self.__communicator.shutdown())
            if len(sys.argv) > 1:
                print(sys.argv[0] + ": too many arguments")
                sys.exit(1)
            if self.__adapter is None:
                self.__adapter = self.__communicator.createObjectAdapter("Manager")

    def getCommunicator(self):
        return self.__communicator

    def addServer(self, cls_inst, comp_name, str_identity):
        identity = Ice.stringToIdentity(comp_name)
        if self.__adapter.find(identity) is None:
            self.__adapter.add(cls_inst, identity)
            self.__adapter.activate()
            return 0
        return 1
        #self.__communicator.waitForShutdown()

     
    def wait(self):
        self.__communicator.waitForShutdown()


