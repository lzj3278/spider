#! -*- coding=utf-8 -*-
import logging
logging.basicConfig(level=logging.INFO)


# def checkParams(fn):
#    def wrapper(a, b):
#        if isinstance(a, (int, float)) and isinstance(b, (int, float)):
#            return fn(a, b)
#
#        logging.warning("variable'a'and 'b' cannot be added ")
#        print 'bad'
#        return
#    return wrapper
#
#
# @checkParams
# def add(a, b):
#    return a + b
#
# if __name__ == "__main__":
#    # add = checkParams(add)
#    add(3, 'hello')

# def deco(func):
# print("before myfunc() called.")
# func()
# print("after myfunc() called.")
# return func

def deco(func):
    def _deco(a, b):
        print "before"
        func(a, b)
        print "after"

    return _deco


@deco
def myfunc(a, b):
    print ("myfunc() called.")
    print "sum = %s +%s" % (a, b)
    return "ok"


# deco(myfunc)
print '+++++++'
myfunc(1, 2)
print '+++++++'
myfunc()
