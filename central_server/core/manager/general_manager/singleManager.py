from threading import Lock, Thread
import json
from core.metasingleton import SingletonMeta

class singleManager(metaclass=SingletonMeta):
    references = {}
    def addRef(self, name, origin, md_name, cls_name, descriptionpath, protected):
        if name not in self.references:
            self.references[name] = {'name': name, 'reference': origin, 'middleware': md_name, 'cls_name': cls_name , 'descriptionpath': descriptionpath, 'protected': protected}
            print(self.references)
            return 0 
        return 1

    def findRefByName(self, name, md_name):
        if name in self.references:
            if not self.references[name]['protected']:
                ret_ref = json.loads(json.dumps(self.references[name]))
                del ret_ref['protected']
                ret_ref = json.dumps(ret_ref)
                return ret_ref
        return None

