# Copyright (c) 2016 Arista Networks, Inc.  All rights reserved.
# Arista Networks, Inc. Confidential and Proprietary.
import arstCliLib
from arstCliLib import openSshOnDut
from arstCliLib import closeSshOnDut
from arstCliLib import sendCmd

#DutName=input("Enter yout Dut Name?")
#print(DutName)
import sys

if len(sys.argv) != 3:
   print("Please enter Dut name and command as an argument to this script")
   print("exiting sript...")
   exit()
else:
   Dut=sys.argv[1]
   Cmd=str(sys.argv[2])
   cmdList=[]
   cmdList.append(Cmd)


#Dut='fm109'
#cmdList=['Show vlan']
   openSshOnDut(Dut, sshUsername='admin', sshPassword='', cliTimeout=30 )
   Result=sendCmd (Dut, cmdList, accessMethod='ssh', prompt='base')
   closeSshOnDut(Dut)
#print(Result[0])
   for list1 in Result:
      for list2 in list1:
         listS2=[]
         for list3 in list2:
            listS2.append(str(list3))
      
         l=len(listS2)
         i=0
         while i < l:
            #i=i+1
            print(listS2[i]),
            i=i+1
         print("")
      #print(listS2)

   exit()
