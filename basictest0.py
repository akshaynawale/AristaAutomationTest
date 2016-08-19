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

def ParseCfgFile(CfgFileName):
	CommandList=[]
	FileHandle=open(CfgFileName)
	for Line in FileHandle:
		if Line:
			if "DUT:" in Line:
				DutLine=Line.strip("DUT:")
				DutLine=DutLine.rstrip()
				DutNames=DutLine.split(",")
			if "Command:" in Line:
				CommandLine=Line.strip("Command:")
				CommandLine=CommandLine.rstrip()
				CommandList.append(CommandLine)
	return DutNames, CommandList

def FireCommand(Command):
	dut="fm109"
	cmdList=[]
	cmdList.append(Command)
	result=capiCmd( dut, cmdList, capiUsername='admin', capiPassword='', capiProtocol='http', capiFormat='json' )	
	#print(result)
	ResultDict=result[0]
	#print(ResultDict)
	print(ResultDict["version"])
	#print(result[0])

CfgFileName=GetCfgFileName()
print(CfgFileName)
DutNames, CommandList=ParseCfgFile(CfgFileName)
print(DutNames, CommandList)
FireCommand("show version")

