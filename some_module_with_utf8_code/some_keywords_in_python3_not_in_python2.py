"""
An easy way to spot differences between Python 2 and Python 3 is to look at the parsers in pygments:
https://bitbucket.org/birkenfeld/pygments-main/src/c65e535ed0dc07aab2f72210b245113ed04bdccd/pygments/lexers/python.py?at=default&fileviewer=file-view-default
"""

import time

def run_comparison():
    """Comparison between bytes and memoryview taken from:
       http://stackoverflow.com/questions/18655648/what-exactly-is-the-point-of-memoryview-in-python
    """
    
    for n in (100000, 200000, 300000, 400000):
        data = 'x'*n
        start = time.time()
        b = data
        while b:
            b = b[1:]
        print('bytes', n, time.time()-start)

    for n in (100000, 200000, 300000, 400000):
        data = 'x'*n
        start = time.time()
        b = memoryview(data)
        while b:
            b = b[1:]
        print('memoryview', n, time.time()-start)