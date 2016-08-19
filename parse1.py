# Copyright (c) 2016 Arista Networks, Inc.  All rights reserved.
# Arista Networks, Inc. Confidential and Proprietary.

import sys
import os.path
from arstCliLib import *
import json
import time


MatchDict={'routerId':"2.2.2.2", 'adjacencyState':"full"}
#MatchDict={"modelName": "DCS-7280SE-64-F","internalVersion": "4.17.1F-3366072.ildecaturap"}
#MatchDict={"hwAddress": "001c.73e0.d461","address": "fe80::21c:73ff:fee0:d461","interface": "Po4"}

def GetCommandName():
        if len(sys.argv) != 2:
                print("this program requires arista command as argument ")
                exit()
        else:
                CommandName=sys.argv[1]
                return CommandName


def FireOnDut(CommandName):
   dut="lf231"
   CmdList=["enable"]
   CmdList.append(CommandName)
   openCapiOnDut( dut, capiUsername='admin', capiPassword='', capiProtocol='http', capiFormat='json' )
   result=capiCmd( dut, CmdList, capiUsername='admin', capiPassword='', capiProtocol='http', capiFormat='json' )
   closeCapiOnDut( dut ) 
   return result
   #resultNew=result[1]['vrfs']['default']['instList']['1']['ospfNeighborEntries']
   
def Subsetof(Big, Small):
   present=True
   for item in Small:
      if item not in Big:
         present=False
   return present

def CompareDicts(Big,Small):
   Match=True
   for key in Small.keys():
      if Small[key]!=Big[key]:
         Match=False
   return Match


def FindKamachiDict(result):
   #print type(result)
   if type(result)== list :
      #print "this is a list"
      for item in result:
         FindKamachiDict(item)


   elif type(result)== dict :
     # print("this is a dict")
      if (Subsetof(result.keys(),MatchDict.keys())):
         #print(result)
         #print("sapadala na bhau")
         Matched=CompareDicts(result, MatchDict)
         if Matched == True:
            print "jinkalas bhava"
            print(result)
      else:
         for key in result.keys():
            FindKamachiDict(result[key])

      



CommandName=GetCommandName()
#print(CommandName)
print(MatchDict)
print("*"*13)
result=FireOnDut(CommandName)
print(result)

FindKamachiDict(result)



