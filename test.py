from _lib import *
__UNDEFINED = object()

class __Optimum_Object_BASE:
    def __getitem__(self, item):
        return getattr(self, item, None)
    def __setitem__(self, item):
        return setattr(self, item, None)
    
class __Optimum_Object_0(__Optimum_Object_BASE):
    def __new__(cls, n):
        if (n<2):
            return n
            
        a=0
        b=1
        c=0
        for i,i in enumerate(range(2,n+1)):
            c=a+b
            a=b
            b=c
            
        return b
fibonacci = __Optimum_Object_0

# Class definition was here
print(fibonacci(9))
