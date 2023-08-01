import sys, os, time
sys.path.append(os.path.join(os.path.dirname(__file__), '.'))
import CORBADemo, CORBADemo__POA


class CORBAHelloI(CORBADemo__POA.Hello):
    def __init__(self):
        self.__counter = 0

    def sayHello(self, delay):
        if delay != 0:
            time.sleep(delay / 1000.0)
        print("Hello World from CORBA!")

    def incCounter(self):
        self.__counter+=1
        return self.__counter

    def shutdown(self, current):
        pass
