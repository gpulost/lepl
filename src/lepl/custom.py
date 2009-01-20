
from threading import local


class Namespace(local):
    
    def __init__(self):
        super().__init__()
        self.__stack = [{}]
        
    def push(self, extra={}):
        self.__stack.append(dict(self.current()))
        for name in extra:
            self.set_opt(name, extra[name])
        
    def pop(self):
        self.__stack.pop(-1)
        
    def __enter__(self):
        self.push()
        
    def __exit__(self, *args):
        self.pop()
        
    def current(self):
        return self.__stack[-1]
    
    def set(self, name, value):
        self.current()[name] = value
        
    def set_opt(self, name, value):
        if value != None:
            self.set(name, value)
        
    def get(self, name, default):
        return self.current().get(name, default)
    

NAMESPACE = Namespace()

SPACE_OPT = '/'
SPACE_REQ = '//'
ADD = '+'
AND = '&'
OR = '|'
APPLY = '>'
NOT = '~'
ARGS = '*'
KARGS = '**'
RAISE = '^' 


class Extension():
    
    def __init__(frame):
        self.__frame = frame
        
    def __enter__(self):
        NAMESPACE.push(self.__frame)
        
    def __exit__(self, *args):
        NAMESPACE.pop()


class Override(Extension):

    def __init__(space_opt=None, space_req=None, 
                  add=None, and_=None, or_=None, not_=None, 
                  apply=None, args=None, kargs=None, raise_=None):
        super().__init__({SPACE_OPT: space_opt, SPACE_REQ: space_req,
                          ADD: add, AND: and_, OR: or_, NOT: not_,
                          APPLY: apply, ARGS: args, KARGS: kargs, RAISE: raise_})


class Extend(Extension):
    
    def __init__(**kargs):
        super().__init__(kargs)
        

    