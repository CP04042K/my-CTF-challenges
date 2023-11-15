#!/usr/local/bin/python

import pickle, io, sys
from pickle import PROTO, NEWOBJ, NEWOBJ_EX, REDUCE, STACK_GLOBAL, GLOBAL, BUILD
import jinja2

ATTR_FORBIDEN_EXCEPTION = Exception("This attribute cannot be loaded")
CANNOT_FIND_MODULE_EXCEPTION = Exception("Cannot find requested module")
MAX_DEPTH_EXCEED_EXCEPTION = Exception("You're so greedy...")
del pickle.Unpickler

def _getattribute(obj, name):
    if name.count(".") > 2:
        raise MAX_DEPTH_EXCEED_EXCEPTION
    for subpath in name.split('.'):
        if subpath == '<locals>':
            raise AttributeError("Can't get local attribute {!r} on {!r}"
                                 .format(name, obj))
        try:
            parent = obj
            obj = getattr(obj, subpath)
        except AttributeError:
            raise AttributeError("Can't get attribute {!r} on {!r}"
                                 .format(name, obj)) from None
    return obj, parent


class Hardening_Unpickler(pickle._Unpickler):
        
    def load_proto(self, parent):
        proto = self.read(1)[0]

        if not 0 <= proto <= 2:
            raise ValueError("unsupported pickle protocol")
        self.proto += proto
        
    def find_class(self, module: str, name: str):
        module = "__main__"
        forbiden_attrs = ["sys", "open", "eval", "exec", "import", "getattribute", "compile", "load", "builtin", "close", "sub", "mod", "chown", "read", "dir", "global", "local", "write", "platform"]
        
        for attr in forbiden_attrs:
            if attr in name:
                raise ATTR_FORBIDEN_EXCEPTION

        if self.proto < 4:
                raise Exception("PROTOCOL NOT SUPPORTED")
        __import__(module, level=0)
        from sys import modules
        if self.proto == 5:
            tmp = _getattribute(modules[module], name)[0]
            return tmp
        else:
            tmp = getattr(modules[module], name)
            return tmp


    def __getattribute__(self, __name: str):
        if __name == "dispatch":
            dispatcher = super().__getattribute__("dispatch")
            dispatcher[PROTO[0]] = self.load_proto
            dispatcher[NEWOBJ[0]] = None
            dispatcher[NEWOBJ_EX[0]] = None
            dispatcher[REDUCE[0]] = None
            dispatcher[STACK_GLOBAL[0]] = None
            dispatcher[GLOBAL[0]] = None
            dispatcher[BUILD[0]] = None
            return dispatcher
        return super().__getattribute__(__name)




sys.stdout = open("/dev/null", "w")
sys.stderr = open("/dev/null", "w")
del sys


while True:
    input_data = io.BytesIO(bytes.fromhex(input()))
    result = Hardening_Unpickler(input_data).load()
    