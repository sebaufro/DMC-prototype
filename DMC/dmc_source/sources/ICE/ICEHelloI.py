#!/usr/bin/env python
#
# Copyright (c) ZeroC, Inc. All rights reserved.
#
import sys, os, time
import Ice

Ice.loadSlice(os.path.join(os.path.dirname(os.path.realpath(__file__)),'Hello.ice'))
import Demo


sys.modules["main"] = sys.modules["__main__"]



class ICEHelloI(Demo.Hello):
    def __init__(self):
        self.__counter = 0

    def sayHello(self, delay, current):
        if delay != 0:
            time.sleep(delay / 1000.0)
        print("Hello World from ICE!")

    def incCounter(self, current):
        self.__counter+=1
        return self.__counter

    def shutdown(self, current):
        current.adapter.getCommunicator().shutdown()

