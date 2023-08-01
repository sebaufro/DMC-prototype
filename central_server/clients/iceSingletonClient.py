import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '.'))
import signal
import Ice
from core.manager.ICE.ICEManager_ice import *
from core.metasingleton import SingletonMeta
import importlib



class iceSingletonClient(metaclass=SingletonMeta):
    __adapter = None
    __communicator = None
    __md_name = "ICEMGR"
    __local_reference = None
    __central_reference = None
    __local_manager_obj = None
    __central_manager_obj = None

    def __init__(self, local_ip, central_ip):
        self.__md_name_central= self.__md_name +"_"+ central_ip.replace('.',"_")
        self.__md_name_local= self.__md_name +"_"+ local_ip.replace('.',"_")
        self.__central_ref = "%s:default -p 10000 -h %s" % (self.__md_name_central, central_ip)
        self.__local_ref = "%s:default -p 10000 -h %s" % (self.__md_name_local, central_ip)


    def getLocalManager(self):
        self.__local_manager_obj, self.__local_ref = self.__startManager(self.__local_ref)
        return {'manager': self.__local_manager_obj, 'reference': self.__local_ref}

    def getCentralManager(self):
        self.__central_manager_obj, self.__local_ref = self.__startManager(self.__central_ref)
        return {'manager': self.__central_manager_obj, 'reference': self.__central_ref}


    def __startManager(self, proxy_ref):
        if self.__communicator is None:
            self.__communicator = Ice.initialize(sys.argv)
        reference = self.__communicator.stringToProxy(proxy_ref)
        manager_obj = ManagerRef.ManagerPrx.checkedCast(reference)
        reference = reference.ice_toString()
        if not reference:
            raise RuntimeError("Invalid proxy")
        return manager_obj, reference

    def getComponentInstance(self, ref):
        proxy = ref['reference']
        if proxy is not None:
            descriptionpath = ref['descriptionpath']
            Ice.loadSlice(os.path.join(*["sources",ref['middleware'], "%s.ice" % descriptionpath.split("/")[-1]]))
            exec("import %s" % (descriptionpath.split("/")[0]))
            
            obj = (descriptionpath.replace("/",'.'))+"Prx"
            return (eval(obj)).checkedCast(self.getCommunicator().stringToProxy(proxy))
        return None

    def getLocalRef(self):
        return self.__local_ref

    def getCentralName(self):
        return self.__md_name_central

    def getLocalName(self):
        return self.__md_name_local

    def getCentralName(self):
        return self.__md_name_central



    def getCommunicator(self):
        return self.__communicator


    def close(self):
        self.__communicator.destroy()


