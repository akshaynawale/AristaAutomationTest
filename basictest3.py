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
	
def InitialConfig(Pointer,TestcaseList):
	Pointer+=1
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
                                	print(dut)
                                	openCapiOnDut( dut, capiUsername='admin', capiPassword='', capiProtocol='http', capiFormat='json' )
                                	result=capiCmd( dut, CmdList, capiUsername='admin', capiPassword='', capiProtocol='http', capiFormat='json' )
                                	closeCapiOnDut( dut )
                                	#print(result)
                        	break	


CfgFileName=GetCfgFileName()
TestcaseList, DutList, Pointer=GetInitialPointer(CfgFileName)
InitialConfig(Pointer, TestcaseList)
TotalSteps=0
StepsList=[]
for i in range(0, len(TestcaseList)):
	line=TestcaseList[i]
	#print(line[:6])
	if line[:6]=="STEP::":
		TotalSteps+=1
		StepsList.append(line[:7])
print("Testcase has "+str(TotalSteps)+" steps")		
#print(StepsList)

for step in StepsList :
	Pointer=TestcaseList.index(step)
	CommandList=[]
	MatchList=[]
	CheckList=[]
	CommandFound=False
	MatchFound=False
	
	while TestcaseList[Pointer] != "///":
		Pointer+=1
		line=TestcaseList[Pointer]
		#print(line[:8])	
		#print(line.startswith("Command:"))
		while TestcaseList[Pointer].startswith("Command:") :
			line=TestcaseList[Pointer]
			line=line.strip("Command:")
			linesplit=line.split("/")
			print(linesplit)
			unit={}
			unit[linesplit[0]]=linesplit[1]	
			CommandList.append(unit)	
			Pointer+=1
			CommandFound=True
		while line.startswith("Match:") :
                        line=line.strip("Match:")
                        linesplit=line.split("=")
                        MatchList.append({linesplit[0]:linesplit[1]})
                        Pointer+=1
                        MatchFound=True
		while line.startswith("Check:") :
                        line=line.strip("Check:")
                        linesplit=line.split("=")
                        CheckList.append({linesplit[0]:linesplit[1]})
                        Pointer+=1
                        MatchFound=True
		if CommandFound :
			CommandFound=False
			CmdList=[]
			print(CommandList)
			for command in CommandList:
                        	for key in command:
                                	dut=key
                                        CmdList.append(command[key])
                                        openCapiOnDut( dut, capiUsername='admin', capiPassword='', capiProtocol='http', capiFormat='json' )
                                        Result=capiCmd( dut, CmdList, capiUsername='admin', capiPassword='', capiProtocol='http', capiFormat='json' )
       	                                closeCapiOnDut( dut )
	#		if MatchFound :
	print(Result)
	#print(CommandList)	
