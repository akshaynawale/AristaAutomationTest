# Copyright (c) 2016 Arista Networks, Inc.  All rights reserved.
# Arista Networks, Inc. Confidential and Proprietary.

import sys
import os.path
from arstCliLib import *
import json
import time


#MatchDict={"vrfs":"", "default":"","instList":"",'routerId':"2.2.2.2", 'adjacencyState':"full"}
#MatchDict={"vrfs":"","instList":"",'routerId':"2.2.2.2", 'adjacencyState':"full"}
#MatchDict={"modelName": "DCS-7280SE-64-F","internalVersion": "4.17.1F-3366072.ildecaturap"}
#MatchDict={"hwAddress": "001c.73e0.d461","address": "fe80::21c:73ff:fee0:d461","interface": "Po4"}
#MatchDict={"Ethernet1":"","name": "Ethernet1","urpf": "disable","interfaceStatus": "connected","mtu": 1500}
MatchDict={"vrfs":"","default":"","routes":"","203.29.0.0/24":"","nexthopAddr": "20.100.200.2"}

def GetCommandName():
        if len(sys.argv) != 2:
                print("this program requires arista command as argument ")
                exit()
        else:
                CommandName=sys.argv[1]
                return CommandName


def FireOnDut(CommandName):
   dut="tg218"
   CmdList=["enable"]
   CmdList.append(CommandName)
   openCapiOnDut( dut, capiUsername='admin', capiPassword='', capiProtocol='http', capiFormat='json' )
   result=capiCmd( dut, CmdList, capiUsername='admin', capiPassword='', capiProtocol='http', capiFormat='json' )
   closeCapiOnDut( dut ) 
   return result
   #resultNew=result[1]['vrfs']['default']['instList']['1']['ospfNeighborEntries']
   
def Subsetof(Big, Small):
   present=0
   for item in Small:
      if item in Big:
         present+=1
   return present

def CompareDicts(Big,Small):
   Match=True
   for key in Small.keys():
      if Small[key]!=Big[key]:
         Match=False
   return Match

def RemoveKeyFromMatchDict(result,MatchDict):
   for key in MatchDict.keys():
      if key in result.keys():
         del MatchDict[key]
         SpecialKey=key
   return MatchDict, SpecialKey


def FindKamachiDict(result, MatchDict):
   #print type(result)
   if type(result)== list :
      #print "this is a list"
      for item in result:
         FindKamachiDict(item, MatchDict)
   elif type(result)== dict :
     # print("this is a dict")
      #print(type(MatchDict))
      if (Subsetof(result.keys(), MatchDict.keys()) == len(MatchDict.keys())):
         #print(result)
         #print("sapadala na bhau")
         Matched=CompareDicts(result, MatchDict)
         if Matched == True:
            print "jinkalas bhava"
            print(result)
      elif Subsetof(result.keys(),MatchDict.keys()) != 0 :
         print("ekach match zala watat")
         MatchDict, SpecialKey  = RemoveKeyFromMatchDict(result,MatchDict)
         result=result[SpecialKey]
         FindKamachiDict(result, MatchDict)
      else:
         for key in result.keys():
            FindKamachiDict(result[key], MatchDict)


#MatchDict={"Ethernet1":"","name": "Ethernet1","urpf": "disable","interfaceStatus": "connected","mtu": 1500}

CommandName=GetCommandName()
#print(CommandName)
print(MatchDict)
print("*"*13)
result=FireOnDut(CommandName)
print(result)

FindKamachiDict(result, MatchDict)



