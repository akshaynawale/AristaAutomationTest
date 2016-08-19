import sys
import os.path
from arstCliLib import *
import json 
import time

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
	print("Testcase execution started :"+CfgFileName)
	Dutline=lines[Pointer-1]
	try:
		Dutline=Dutline.strip("DUT:")
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
                                	#print(CmdList)
                                	#print(dut)
                                	openCapiOnDut( dut, capiUsername='admin', capiPassword='', capiProtocol='http', capiFormat='json' )
                                	result=capiCmd( dut, CmdList, capiUsername='admin', capiPassword='', capiProtocol='http', capiFormat='json' )
                                	closeCapiOnDut( dut )
                                	#print(result)
                        	break	


def CompareDict(Big, Small):
	Count=0
	for keyS in Small:
		for keyB in Big:
			if keyS == keyB :
				if  type(Small[keyS]) != type(Big[keyB]):
                                	ValueS=str(Small[keyS])
                                	ValueB=str(Big[keyB])
                        	else:
                                	ValueS=Small[keyS]
                                	ValueB=Big[keyB]
				if ValueS==ValueB :
			
					Count+=1
	if Count == len(Small):
		#print("mar tichya")		
		return True
			
	else:
		return False

def DisplayResult(CfgFileName, StepStatus, NormalResultList, MatchDict, CheckDict, step):
        #print("In Display result na bhau")
	if StepStatus=="PASS":
		print("Match parameters:")
                print(MatchDict)
                print("Check Parameters:")
                print(CheckDict)
                print(str(step)+" in testcase "+CfgFileName+" is passed" )
		print("\n")
        elif StepStatus=="FAIL":
                print("Error Dump for this step:")
                print("Result List:")
                print(NormalResultList)
                print("Match Dictionary:")
                print(MatchDict)
                print("Check Dictionary:")
                print(CheckDict)
		print(str(step)+" in testcase "+CfgFileName+" is failed" )
        elif StepStatus=="MatchNotFound":
                print(str(step)+" in testcase "+CfgFileName+" is wrong or match not found" )
        elif StepStatus=="UNKNOWN":
                print(str(step)+" in testcase "+CfgFileName+" is not executed " )
         
def GetTestcaseFlow(TestcaseList):
   StepList=[]
   for i in range(0, len(TestcaseList)):
      line=TestcaseList[i]
      if line[:6]=="STEP::":
         StepName=line.rstrip()
         StepList.append(StepName)
      #print(line[:7])
      if line[:7] == "Repeat=" :
         StepListLine=line[7:]
         #print(StepListLine)
         StepListSplit=StepListLine.split("=")
         StepListRepeat=int(StepListSplit[0])
         StepListLine=StepListSplit[1]
         StepListSplit=StepListLine.split("+")
         #print(StepListSplit)
         j=0
         #print(str(StepListRepeat))
         while j < StepListRepeat:
            for StepName in StepListSplit:
               StepList.append(StepName) 
            j+=1
      #else:
         #StepList.append(StepName)

   return StepList
                  


CfgFileName=GetCfgFileName()
TestcaseList, DutList, Pointer=GetInitialPointer(CfgFileName)
InitialConfig(Pointer, TestcaseList)
StepList=GetTestcaseFlow(TestcaseList)
TotalSteps=len(StepList)
print("Testcase has "+str(TotalSteps)+" steps")		
NRepeat=0
RepeatAlreadyFound=False
print(StepList)
TestcaseStatus=[]

for step in StepList :
	StepStatus="UNKNOWN"
	Pointer=TestcaseList.index(step)
	CommandList=[]
	MatchDict={}
	CheckDict={}
	NormalResultList=[]
	while (TestcaseList[Pointer] != "///") :
		Pointer+=1
		line=TestcaseList[Pointer]
		CommandFound=False
		MatchFound=False
		DelayTime=0
		while TestcaseList[Pointer].startswith("Command:") :	
			line=TestcaseList[Pointer]
			line=line[8:]
			linesplit=line.split("=")
			unit={}
			unit[linesplit[0]]=linesplit[1]	
			CommandList.append(unit)	
			Pointer+=1
			CommandFound=True
		Delay=False
		if TestcaseList[Pointer].startswith("Delay:") :
			Delay=True
			line=TestcaseList[Pointer]
                        line=line.strip("Delay:")
                        DelayTime=int(line)
			#print("Delay found time for delay is "+str(DelayTime))
		if Delay == False:
			while TestcaseList[Pointer].startswith("Match:") :
                        	line=TestcaseList[Pointer]
				line=line.strip("Match:")
                        	linesplit=line.split("=")
                        	MatchDict[linesplit[0]]=linesplit[1]
                        	Pointer+=1
                        	MatchFound=True
			while TestcaseList[Pointer].startswith("Check:") :
                        	line=TestcaseList[Pointer]
				line=line.strip("Check:")
                        	linesplit=line.split("=")
                        	CheckDict[linesplit[0]]=linesplit[1]
                        	Pointer+=1
                        	MatchFound=True
		
		if CommandFound :
			CommandFound=False
			CmdList=[]
			for command in CommandList:
                        	for key in command:
                                	dut=key
                                        CmdList.append(command[key])
			openCapiOnDut( dut, capiUsername='admin', capiPassword='', capiProtocol='http', capiFormat='json' )
                        Result=capiCmd( dut, CmdList, capiUsername='admin', capiPassword='', capiProtocol='http', capiFormat='json' )
       	                closeCapiOnDut( dut )
			#print(Result)
                        if Delay :			
				time.sleep(DelayTime)
				StepStatus="PASS"
				CommandList=[]
		
                if MatchFound :
			ResultDict=Result[1]
                        #print(ResultDict)
			for key in ResultDict:
				ResultList=ResultDict[key]
				
			unique=0
			MyDict={}
                        #print(ResultList)                        
			for dict in ResultList:
				NormalDict={}
				for key in dict:
					if type(key)== unicode: 
						NonUnicodeKey=key.encode("utf-8")
						if type(dict[key])== unicode:
							NonUnicodeValue=dict[key].encode("utf-8")
							NormalDict[NonUnicodeKey]=NonUnicodeValue
						elif type(dict[key]) == list :
                                                        NonUnicodeValueList=[]
                                                        for l in dict[key]:
                                                                if type(l) == unicode:
                                                                        NonUnicodeValueList.append(l.encode("utf-8"))
							NonUnicodeValueTuple=tuple(NonUnicodeValueList)
                                                        NormalDict[NonUnicodeKey]=NonUnicodeValueTuple
						else:
							NormalDict[NonUnicodeKey]=dict[key]
					else:
                                                #print(key)
                                                #print(dict[key])
                                                #print(type(key))
						NormalDict[key]=dict[key]
				NormalResultList.append(NormalDict)
			for dict in NormalResultList:
				if CompareDict(dict, MatchDict):
					if CompareDict(dict, CheckDict):
						StepStatus="PASS"
					else:
						StepStatus="FAIL"
				else:
					StepStatus="MachNotFound"
                                        """
		if TestcaseList[Pointer].startswith("Repeat="):
			if RepeatAlreadyFound == False:
				print("Repeat first time found")
				RepeatAlreadyFound=True
				print(RepeatAlreadyFound)
				line=TestcaseList[Pointer]
                        	line=line.strip("Repeat=")
				RepeatSplit=line.split("=")
                        	Repeat=int(RepeatSplit[0])
				RepeatStartStep=RepeatSplit[1]
				Pointer=TestcaseList.index(RepeatStartStep)
                                step=RepeatStartStep
				Repeat=Repeat-2
				print(Repeat)
			else:
				print(Repeat)
				if Repeat != 0:
					DisplayResult(CfgFileName, StepStatus, NormalResultList, MatchDict, CheckDict, step)
					("Repeating the step.. still "+str(Repeat)+" repeats are remaining")
					Pointer=TestcaseList.index(RepeatStartStep)
					Repeat=Repeat-1
					print("He He")
					RepeatAlreadyFound==True
				else:
					DisplayResult(CfgFileName, StepStatus, NormalResultList, MatchDict, CheckDict, step)
					print("repeat completed")
					RepeatAlreadyFound=False
"""		
	DisplayResult(CfgFileName, StepStatus, NormalResultList, MatchDict, CheckDict, step)		
        TestcaseStatus.append(StepStatus)

print(TestcaseStatus)
exit()
