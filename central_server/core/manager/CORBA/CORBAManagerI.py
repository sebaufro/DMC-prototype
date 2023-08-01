import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '.'))

from core.manager.general_manager.singleManager import singleManager
from core.referencesclass import ReferencesClass

from core.manager.CORBA.CORBAManager_idl import *



class CORBAManagerI(CORBAManagerRef__POA.Manager):
    def __init__(self, local_address, server=None):
        self.__manager = singleManager()
        self.__md_name = "CORBA"
        self.__refUpdater = ReferencesClass()
        if server is None:
            self.__corbaServerRef = None
        else:
            from servers.corbaSingletonServer import corbaSingletonServer
            self.__corbaServerRef = corbaSingletonServer()
        self.__local_address = local_address

    def addRef(self, comp_name, str_identity, cls_name, descriptionpath, protected=False):
        identity = str(str_identity)
        return self.__manager.addRef(comp_name, identity, self.__md_name, cls_name, descriptionpath, protected)

    def findRefByName(self, comp_name):
        print("---addObjToServer---")
        ref = self.__manager.findRefByName(comp_name, self.__md_name)
        if ref is not None:
            return ref
        else:
            raise CORBAManagerRef.notFoundRef

    def addObjToServer(self, comp_name, cls_name):
        if self.__corbaServerRef is not None:
            if cls_name not in self.__refUpdater.imported:
                print(cls_name)
                self.__refUpdater.importModule(cls_name, [self.__md_name])
            if cls_name in self.__refUpdater.imported:
                str_identity = self.__local_address
                identity = str_identity
                val =  str(self.__refUpdater.imported[cls_name].__bases__)
                descriptionpath = val.split("'")[1].replace(".","/")
                rsp = self.__corbaServerRef.addServer(self.__refUpdater.imported[cls_name](), comp_name, identity)
                self.addRef(comp_name, identity, cls_name, descriptionpath, False)
                return 0
            else:
                raise CORBAManagerRef.notFoundClass
        else:
            print("Unsupported operation")


    def addObjInstance(self):
        pass


    def findRefsDefs(self, comp_name):
        ref = "test"
        return "findRefsDefs"

    def shutdown(self, current):
        #current.adapter.getCommunicator().shutdown()
        pass



