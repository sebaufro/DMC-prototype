# Python stubs generated by omniidl from Hello.idl
# DO NOT EDIT THIS FILE!

import omniORB, _omnipy
from omniORB import CORBA, PortableServer
_0_CORBA = CORBA


_omnipy.checkVersion(4,2, __file__, 1)

try:
    property
except NameError:
    def property(*args):
        return None


#
# Start of module "CORBADemo"
#
__name__ = "CORBADemo"
_0_CORBADemo = omniORB.openModule("CORBADemo", r"Hello.idl")
_0_CORBADemo__POA = omniORB.openModule("CORBADemo__POA", r"Hello.idl")


# interface Hello
_0_CORBADemo._d_Hello = (omniORB.tcInternal.tv_objref, "IDL:CORBADemo/Hello:1.0", "Hello")
omniORB.typeMapping["IDL:CORBADemo/Hello:1.0"] = _0_CORBADemo._d_Hello
_0_CORBADemo.Hello = omniORB.newEmptyClass()
class Hello :
    _NP_RepositoryId = _0_CORBADemo._d_Hello[1]

    def __init__(self, *args, **kw):
        raise RuntimeError("Cannot construct objects of this type.")

    _nil = CORBA.Object._nil


_0_CORBADemo.Hello = Hello
_0_CORBADemo._tc_Hello = omniORB.tcInternal.createTypeCode(_0_CORBADemo._d_Hello)
omniORB.registerType(Hello._NP_RepositoryId, _0_CORBADemo._d_Hello, _0_CORBADemo._tc_Hello)

# Hello operations and attributes
Hello._d_sayHello = ((omniORB.tcInternal.tv_short, ), (), None)
Hello._d_incCounter = ((), (omniORB.tcInternal.tv_long, ), None)
Hello._d_shutdown = ((), (), None)

# Hello object reference
class _objref_Hello (CORBA.Object):
    _NP_RepositoryId = Hello._NP_RepositoryId

    def __init__(self, obj):
        CORBA.Object.__init__(self, obj)

    def sayHello(self, *args):
        return self._obj.invoke("sayHello", _0_CORBADemo.Hello._d_sayHello, args)

    def incCounter(self, *args):
        return self._obj.invoke("incCounter", _0_CORBADemo.Hello._d_incCounter, args)

    def shutdown(self, *args):
        return self._obj.invoke("shutdown", _0_CORBADemo.Hello._d_shutdown, args)

omniORB.registerObjref(Hello._NP_RepositoryId, _objref_Hello)
_0_CORBADemo._objref_Hello = _objref_Hello
del Hello, _objref_Hello

# Hello skeleton
__name__ = "CORBADemo__POA"
class Hello (PortableServer.Servant):
    _NP_RepositoryId = _0_CORBADemo.Hello._NP_RepositoryId


    _omni_op_d = {"sayHello": _0_CORBADemo.Hello._d_sayHello, "incCounter": _0_CORBADemo.Hello._d_incCounter, "shutdown": _0_CORBADemo.Hello._d_shutdown}

Hello._omni_skeleton = Hello
_0_CORBADemo__POA.Hello = Hello
omniORB.registerSkeleton(Hello._NP_RepositoryId, Hello)
del Hello
__name__ = "CORBADemo"

#
# End of module "CORBADemo"
#
__name__ = "Hello_idl"

_exported_modules = ( "CORBADemo", )

# The end.