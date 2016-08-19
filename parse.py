# Copyright (c) 2016 Arista Networks, Inc.  All rights reserved.
# Arista Networks, Inc. Confidential and Proprietary.

import sys
import os.path
from arstCliLib import *
import json
import time

def GetCommandName():
        if len(sys.argv) != 2:
                print("this program requires arista command as argument ")
                exit()
        else:
                CommandName=sys.argv[1]
                return CommandName


def FireOnDut(CommandName):
   dut="fm109"
   CmdList=["enable"]
   CmdList.append(CommandName)
   openCapiOnDut( dut, capiUsername='admin', capiPassword='', capiProtocol='http', capiFormat='json' )
   result=capiCmd( dut, CmdList, capiUsername='admin', capiPassword='', capiProtocol='http', capiFormat='json' )
   closeCapiOnDut( dut ) 
   #print(result)
   ##print(result[1])
   #print(result[1]['vrfs']['default'])
   #print((result[1]['vrfs']['default']['instList']['1']['ospfNeighborEntries']))
   resultNew=result[1]['vrfs']['default']['instList']['1']['ospfNeighborEntries']
   for entry in resultNew :
      #print(entry['routerId']+" --- "+entry['interfaceName']+" --- "+entry['adjacencyState'])
      for key in entry.keys() :
         if entry
         print(str(key)+" ---> "+str(entry[key]))
      print("+"*10)
   #print(result[1]['details'])
   #FindDeepestDict(result)
   
   """
   for key in result:
      if type(key)== dict :
         for key1 in key :

            print(key[key1])"""
def FindDeepestDict(Result):
   test=Result
   while type(test) == dict or type(test) == list :
      if type(test)==dict:
         for key in test:
            Result=test[key]
      elif type(test) == list:
         for key in test:
            Result=key
   print(test)
CommandName=GetCommandName()
print(CommandName)
#print(CommandName[1])
#print(CommandName[0])
FireOnDut(CommandName)

