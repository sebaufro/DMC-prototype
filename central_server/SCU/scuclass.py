import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), '.'))

from core.utils.utils import *

from clients.iceSingletonClient import iceSingletonClient
from clients.corbaSingletonClient import corbaSingletonClient
from core.referencesclass import ReferencesClass

import traceback, json
'''
Clase de Standar Communication Utilities
implementa la mayoria de las opciones de comunicación, esta clase puede ser aislada
para ser utilizada unicamente como cliente. Se encarga de generar un nexo de comunicación
entre el dispositivo que la ejecuta y el Central Reference Device. Para cada middleware 
soportado, inicia un cliente que corresponde a una instancia remota de un "Manager".
Los manager tienen una serie de metodos que permiten la busqueda e iniciación de componentes 
en la red.
'''
class SCUClass():
	def __init__(self, central_ref = None):
		self._local_address = get_ip_address()
		self._central_manager_ref = checkCentralRef(central_ref)


		self._ref_updater = ReferencesClass()
		self._suppertedMidd = ["ICE", "CORBA"]

		self.__clients = {}
		self._local_clients = {}
		self._central_clients = {}
		
		# Iniciación de cliente ICE y variables necesarias (RF-03)
		self.__clients['ICE'] = iceSingletonClient(self._local_address, self._central_manager_ref)
		self._ice_local_name = self.__clients['ICE'].getLocalName()
		self._ice_central_name = self.__clients['ICE'].getCentralName()
		self._ice_local_mgr_proxy = self.__clients['ICE'].getLocalRef()

		# Iniciación de cliente CORBA y variables necesarias (RF-04)
		self.__clients['CORBA'] = corbaSingletonClient(self._local_address, self._central_manager_ref)
		self._corba_local_name = self.__clients['CORBA'].getLocalName()
		self._corba_central_name = self.__clients['CORBA'].getCentralName()

		self._corba_local_mgr_proxy = self.__clients['CORBA'].getLocalRef()

		
	'''
	Función para iniciar el cliente ICE y obtener una referencia al manager remoto/local
	'''
	def _startICEManager(self):
		info = self.__clients['ICE'].getCentralManager()
		self._central_clients['ICE'] = info['manager']

		info = self.__clients['ICE'].getLocalManager()
		self._local_clients['ICE'] = info['manager']
		self._central_clients['ICE'].addRef(self._ice_local_name, info['reference'], "ICEManagerI", "ManagerRef/Manager", True)

	'''
	Función para iniciar el cliente CORBA y obtener una referencia al manager remoto/local
	'''
	def _startCORBAManager(self):
		info = self.__clients['CORBA'].getCentralManager()
		self._central_clients['CORBA'] = info['manager']

		info = self.__clients['CORBA'].getLocalManager()
		self._local_clients['CORBA'] = info['manager']
		rsp = self._central_clients['CORBA'].addRef(self._corba_local_name, info['reference'], "CORBAManagerI", "ManagerRef/Manager", True)


	'''
	Funcion para importar dinamicamente librerias de python
	@params
	* file: (string) nombre del archivo con implementacion (sin extensioón)
	* subfolder: (string[]) arreglo con todas las subcarpetas donde se encuentra la libreria
	* folder: (string) ombre de la carpeta base donde se encuentra la libreria
	'''
	def _importByName(self, file, sub_folders=None, folder='sources'):
		self._ref_updater.importModule(file, sub_folders, folder)

	'''
	Función para encapsular la selección del middleware que se utilizará
	@params
	* midd: (string/None) nombre del middleware a utilizar
	@return string con el middleware a utilizar
	@comments: falta incorporar mecanismos de verificación
	'''
	def _getMidd(self, midd=None):
		if midd is None:
			return list(self._central_clients.keys())[0]
		else:
			return midd

	'''
	Función para búsqueda de componentes registrados (RF-07)
	@params
	* comp_name: (string) nombre del componente buscado
	* midd: (string) middleware del cliente utilizado
	@return string con referencia del componente/None si no existe o esta protegido (componente privado del sistema)
	'''
	def findComponent(self, comp_name, midd=None):
		midd= self._getMidd(midd)
		try:
			return self._central_clients[midd].findRefByName(comp_name)
		except:
			traceback.print_exc()
			return None


	'''
	Función para instanciación directa de componente (RF-09)
	@params
	* comp_name: (string) nombre del componente buscado
	@return instancia de componente (ICE o CORBA)/ None
	@comments: falta incorporar mecanismos de verificación (middleware no soportado)
	'''
	def getComponentByName(self, comp_name):
		ref = self.findComponent(comp_name)
		if ref is not None:
			ref = json.loads(ref)
			midd = ref['middleware'] 
			return self.__clients[midd].getComponentInstance(ref)
		else:
			None