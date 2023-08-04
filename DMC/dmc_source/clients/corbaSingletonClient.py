import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '.'))
from omniORB import CORBA
import CosNaming
from core.manager.CORBA.CORBAManager_idl import *
import CORBAManagerRef, CORBAManagerRef__POA
from core.metasingleton import SingletonMeta
import importlib.util


class corbaSingletonClient(metaclass=SingletonMeta):
    __adapter = None
    __communicator = None

    __md_name = "CORBAMGR"
    __orb = None
    __poa = None
    __rootContext  = None
    __poaManager = None
    __manager_obj = None
    __reference = None

    def __init__(self, local_ip, central_ip):
        self.__md_name_central= self.__md_name +"_"+ central_ip.replace('.',"_")
        self.__md_name_local= self.__md_name +"_"+ local_ip.replace('.',"_")
        self.__central_ref = central_ip
        self.__local_ref = local_ip

    def getLocalManager(self):
        self.__local_manager_obj, self.__local_ref = self.__startManager(self.__local_ref, self.__md_name_local)
        return {'manager': self.__local_manager_obj, 'reference': self.__local_ref}

    def getCentralManager(self):
        self.__central_manager_obj, self.__central_ref = self.__startManager(self.__central_ref, self.__md_name_central)
        return {'manager': self.__central_manager_obj, 'reference': self.__central_ref}

    def __startManager(self, proxy_ref, name):
        orb = CORBA.ORB_init(["-ORBInitRef", "NameService=corbaname::%s" % proxy_ref] , CORBA.ORB_ID)
        obj         = orb.resolve_initial_references("NameService")
        self.__rootContext = obj._narrow(CosNaming.NamingContext)

        if self.__rootContext is None:
            print ("Failed to narrow the root naming context")
            sys.exit(1)

        name = [CosNaming.NameComponent("test", "my_context"),
                CosNaming.NameComponent(name, name)]
        try:
            obj = self.__rootContext.resolve(name)

        except CosNaming.NamingContext.NotFound:
            print ("Name not found")


        print("---->New CORBA client connected to %s" % proxy_ref)

        manager_obj = obj._narrow(CORBAManagerRef.Manager)
        return manager_obj, proxy_ref

    def getComponentInstance(self, ref):
        proxy = ref['reference']
        if proxy is not None:
            descriptionpath = ref['descriptionpath']
            namespace = [CosNaming.NameComponent("test", "my_context"), CosNaming.NameComponent(ref['name'], ref['name'])]
            try:
                context = self.__rootContext.resolve(namespace)

            except CosNaming.NamingContext.NotFound:
                print ("Name not found")

            module_name = descriptionpath.split("/")[0].replace("__POA","")
            exec("from sources.CORBA.%s import %s, %s" % (ref["cls_name"], module_name, module_name+"__POA"))
            
            # Narrow the object to an Example::Echo
            obj = (descriptionpath.replace("/",'.').replace("__POA",""))
            self.__remoteObj = context._narrow(eval(obj))
            return  self.__remoteObj
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
        return None


    def close(self):
        self.__communicator.destroy()


# Block for ever (or until the ORB is shut down)
#orb.run()
