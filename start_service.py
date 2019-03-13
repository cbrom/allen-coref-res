#/bin/usr/env python
import sys
sys.path.insert(0, 'Service')

from server import *

server = start_server()
_ONE_DAY = 86400

if __name__ == '__main__':    
    try:
        while True:
            time.sleep(_ONE_DAY)
    except KeyboardInterrupt:
        server.stop()