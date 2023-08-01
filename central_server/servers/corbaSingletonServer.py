import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '.'))
from omniORB import CORBA, PortableServer
import CosNaming
from core.metasingleton import SingletonMeta


class corbaSingletonServer(metaclass=SingletonMeta):
    __adapter = None
    __communicator = None
    __orb = None
    __poa = None
    __rootContext  = None
    __poaManager = None
    def __init__(self):
        if self.__rootContext is None:
            argv = ["-ORBInitRef", "NameService=corbaname::172.18.0.2"]
            self.__orb = CORBA.ORB_init(argv, CORBA.ORB_ID)
            self.__poa = self.__orb.resolve_initial_references("RootPOA")
            # Create an instance of Echo_i and an Echo object reference

            # Obtain a reference to the root naming context
            obj = self.__orb.resolve_initial_references("NameService")
            self.__rootContext  = obj._narrow(CosNaming.NamingContext)
            if self.__rootContext is None:
                print ("Failed to narrow the root naming context")
                sys.exit(1)

    def addServer(self, cls_inst, comp_name, str_identity):
        name = [CosNaming.NameComponent("test", "my_context")]
        try:
            testContext = self.__rootContext.bind_new_context(name)
            print ("New test context bound")
        except CosNaming.NamingContext.AlreadyBound:
            print ("Test context already exists")

        obj = self.__rootContext.resolve(name)
        testContext = obj._narrow(CosNaming.NamingContext)
        if testContext is None:
            print ("test.mycontext exists but is not a NamingContext")
            sys.exit(1)

        # Bind the Echo object to the test context
        name = [CosNaming.NameComponent(comp_name, comp_name)]
        try:
            testContext.bind(name, cls_inst._this())
            print ("New %s object bound" % comp_name)
        except CosNaming.NamingContext.AlreadyBound:
            testContext.rebind(name, cls_inst._this())
            print ("%s binding already existed -- rebound" % comp_name)

        if self.__poaManager is None:
            self.__poaManager = self.__poa._get_the_POAManager()
            self.__poaManager.activate()
        return 0
        #self.__communicator.waitForShutdown()

     
    def wait(self):
        pass


# Block for ever (or until the ORB is shut down)
#orb.run()
