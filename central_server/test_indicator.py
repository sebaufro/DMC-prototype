from DMC.dmcclass import DMCClass
import timeit

if "__main__":
	a = DMCClass()
	a.startComponent("hello_corba","CORBAHelloI","CORBA")
	a.startComponent("hello_ice","ICEHelloI","ICE")
	hello_corba = a.getComponentByName("hello_corba")
	hello_ice = a.getComponentByName("hello_ice")

	n = 100000
	result = timeit.timeit(stmt='hello_corba.incCounter()', globals=globals(), number=n)

	print("(CORBA) Tiempo total para %s llamadas remotas: %s" % (n, result) )
	print("(CORBA) Tiempo promedio por llamada remota %s" % (result/n))

	result = timeit.timeit(stmt='hello_ice.incCounter()', globals=globals(), number=n)
	print("(ICE) Tiempo total para %s llamadas remotas: %s" % (n, result) )
	print("(ICE) Tiempo promedio por llamada remota %s" % (result/n))
	
