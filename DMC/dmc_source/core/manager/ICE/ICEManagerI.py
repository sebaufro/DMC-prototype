import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '.'))


from core.manager.general_manager.singleManager import singleManager

from core.referencesclass import ReferencesClass

from ICEManager_ice import *

class ICEManagerI(ManagerRef.Manager):

    def __init__(self, local_address, server=None):
        self.__manager = singleManager()
        self.__md_name = "ICE"
        self.__refUpdater = ReferencesClass()
        if server is None:
            self.__iceServerRef = None
        else:
            from servers.iceSingletonServer import iceSingletonServer
            self.__iceServerRef = iceSingletonServer()
        self.__local_address = local_address

    def addRef(self, comp_name, str_identity, cls_name, descriptionpath, protected = False, current = None):
        identity = str(Ice.stringToIdentity(str_identity))
        identity = str(str_identity)
        return self.__manager.addRef(comp_name, identity, self.__md_name, cls_name, descriptionpath, protected)

    def findRefByName(self, comp_name, current):
        ref = self.__manager.findRefByName(comp_name, self.__md_name)
        if ref is not None:
            return ref
        else:
            raise ManagerRef.notFoundRef

    def addObjToServer(self, comp_name, cls_name, current):
        if self.__iceServerRef is not None:
            if cls_name not in self.__refUpdater.imported:
                self.__refUpdater.importModule(cls_name, [self.__md_name])
            if cls_name in self.__refUpdater.imported:
                str_identity = "%s:default -p 10000 -h %s" % (comp_name, self.__local_address)
                identity = str_identity
                val = str(self.__refUpdater.imported[cls_name].__bases__)
                descriptionpath = val.split("'")[1].replace(".","/")
                rsp = self.__iceServerRef.addServer(self.__refUpdater.imported[cls_name](), comp_name, identity)
                self.addRef(comp_name, identity, cls_name, descriptionpath, False, current)
                return 0
            else:
                raise ManagerRef.notFoundClass
        else:
            print("unsupported operation")
            return 1

    def addObjInstance(self):
        pass


    def findRefsDefs(self, comp_name, current):
        ref = "test"
        print(dir(current))
        print(dir(current.con))
        print(dir(current.adapter))
        com = dir(current.adapter.getCommunicator())
        print(dir(com))
        return "findRefsDefs"

    def shutdown(self, current):
        current.adapter.getCommunicator().shutdown()



