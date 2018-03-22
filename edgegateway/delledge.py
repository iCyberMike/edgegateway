#!/usr/bin/env python

import edgegateway
import sys

def runme():

    arguments = len(sys.argv) - 1  
    print ("the script is called with %i arguments" % (arguments))  

    edge = edgegateway.edgegateway("./aigateway.ini")
    print("edge", edge)
    
    #edgegateway.run()
    edge.run()
    
if __name__ == '__main__':
    runme()
