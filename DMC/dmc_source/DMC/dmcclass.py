import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '.'))

from servers.iceSingletonServer import iceSingletonServer
from servers.corbaSingletonServer import corbaSingletonServer

import traceback

import SCU.scuclass 

'''
Clase de implementación del Distributed Managment Core
esta clase era de SCU. Esta clase se encarga de gestionar los servidores
ICE y CORBA. Todas las acciones son gestionadas mediante managers 
que operan a nivel de red local, esto permite que las diferentes acciones 
pueden ejecutarse localmente o ser invocadas remotamente a traves de ICE o CORBA
'''
class DMCClass(SCU.scuclass.SCUClass):
	'''
	constructor de la clase, se inician los servidores
	'''
	def __init__(self, central_ip=None):
		super().__init__(central_ip)

		# Creación de servidor CORBA (RF-01) 
		self._ice_server_ref = iceSingletonServer(self._central_manager_ref)
		self._startICEEngine()

		# Creación de servidor CORBA (RF-02) 
		self._corba_server_ref = corbaSingletonServer(self._central_manager_ref)
		self._startCORBAEngine()

	
	'''
	Funcion para iniciar manager local en ICE
	'''
	def _startICEEngine(self):
		self._importByName("ICEManagerI", ["manager","ICE"], "core")
		self._ice_server_ref.addServer(self._ref_updater.imported['ICEManagerI'](self._local_address, ''), self._ice_local_name, self._ice_local_mgr_proxy)
		self._startICEManager()


	'''
	Funcion para iniciar manager local en ICE
	'''
	def _startCORBAEngine(self):
		self._importByName("CORBAManagerI", ["manager","CORBA"], "core")
		self._corba_server_ref.addServer(self._ref_updater.imported['CORBAManagerI']( self._local_address, ''), self._corba_local_name, self._corba_local_mgr_proxy)
		self._startCORBAManager()


	'''
	Función para iniciar un componente a nivel local (RF-05), el código fuente debe estar sources/<middleware>/
	@params
	* comp_name: (string) nombre que se le dará al componente 
	* cls_name: (string) nombre de la archivo y clase con el código fuente del componente
	* midd: (string) middleware del cliente utilizado
	@return boolean con resultado existoso (True)/no exitoso (False)

	'''
	def startComponent(self, comp_name, cls_name, midd=None):
		midd= self._getMidd(midd)
		ref = None
		# Se busca si existe la referencia, el resultado esperado es una excepción que indica que el nombre no esta registrado (comp_name)
		try:
			ref = self._central_clients[midd].findRefByName(comp_name)
			if ref is not None:
				print("el componente %s ya se encuentra registrado en el sistema con referencia %s" % (comp_name, ref))
		except:
			pass

		#Si el nombre no esta registrado se intenta agregar el nuevo componente al servidor del middleware seleccionado
		if ref is None:
			try:
				self._central_clients[midd].addObjToServer(comp_name, cls_name)
				return True
			except:
				traceback.print_exc()
		return False


	'''
	inicio de componente remoto (RF-06)
	'''
	def startRemoteComponent(self, comp_name, cls_name, midd=None):
		pass


	'''
	eliminar componente (RF-08)
	'''
	def removeComponent(self, comp_name, midd=None):
		pass


	'''
	Iniciación de múltiples componentes a partir de un único código fuente (RF-10)
	'''

	'''
	Lectura de configuración de inicio (RF-12)
	'''

	'''
	Middlewares modulares (RF-13)
	'''
	def getNewComponent(self, comp_name, cls_name, midd=None):
		pass