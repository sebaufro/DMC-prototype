import os, sys
import importlib.util
from .metasingleton import SingletonMeta
sys.path.append(os.path.join(os.path.dirname(__file__), '.'))
class ReferencesClass(metaclass=SingletonMeta):
	def __init__(self):
		self.imported = {}
		self.__files = []

	def importAll(self, folder):
		pass
	
	def importModule(self, file, sub_folders, folder='sources'):
		custom_class= None
		module = None
		arr_mod = [folder] + sub_folders + [file]
		arr_path = [folder] + sub_folders + ["%s.py" % file]

		file_path = os.path.join(*arr_path)
		if file_path not in self.__files:
			self.__files.append(file_path)
			spec = importlib.util.spec_from_file_location('.', file_path)
			module = importlib.util.module_from_spec(spec)
			spec.loader.exec_module(module)
			m_name = ".".join(arr_mod)
			for x in dir(module):
				if x == file:
					custom_class = getattr(module, x)
					exec("from %s import %s" % (m_name, x))
					globals()[x] = locals()[x]
					self.imported[x] = locals()[x]
			print(self.imported)
