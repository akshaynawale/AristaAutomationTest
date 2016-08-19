# Copyright (c) 2016 Arista Networks, Inc.  All rights reserved.
# Arista Networks, Inc. Confidential and Proprietary.

import sys
import os.path
from arstCliLib import *

def GetCfgFileName():
        if len(sys.argv) != 2:
                print("this program requires cfg file to run testcase please provide filename as argument to this program ")
                exit()
        else:
                CfgFileName=sys.argv[1]
                FilePresent=os.path.isfile(CfgFileName)
                if not FilePresent :
                        print("file not found")
                        exit()
        return CfgFileName

def GetInitialPointer(CfgFileName):
        fh=open(CfgFileName,'r')
        lines=fh.readlines()
        for i in range(0, len(lines)):
                lines[i]=lines[i].rstrip()
        #print(lines)
        Pointer=lines.index("Initial Config:")
        print("testcase execution started")
        Dutline=lines[Pointer-1]
        print(Dutline)
        try:
                Dutline=Dutline.strip("DUT:")
                #print(Dutline)
                DutList=Dutline.split(",")
        except:
                print("problem with Duts in the cfg file")
                exit()
        return(lines, DutList, Pointer)

CfgFileName=GetCfgFileName()
print(CfgFileName)
TestcaseList, DutList, Pointer=GetInitialPointer(CfgFileName)
print(Pointer)
Pointer+=1
DutName=TestcaseList[Pointer].strip(":")
for dut in DutList:
        Pointer=TestcaseList.index((dut+":"))
        Pointer+=1
        CmdList=[]
        while Pointer < len(TestcaseList):
                if TestcaseList[Pointer]!="///":
                        CmdList.append(TestcaseList[Pointer])
                        Pointer+=1
                else:
                        if len(CmdList) != 0:
                                print(CmdList)
                                openCapiOnDut( dut, capiUsername='admin', capiPassword='', capiProtocol='http', capiFormat='json' )
                                result=capiCmd( dut, CmdList, capiUsername='admin', capiPassword='', capiProtocol='http', capiFormat='json' )
                                closeCapiOnDut( dut )
                                print(result)
                        break
