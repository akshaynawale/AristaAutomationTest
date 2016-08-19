import sys
import os.path
from arstCliLib import *
import json 


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


def CompareDict(Big, Small):
	Count=0
	for keyS in Small:
		for keyB in Big:
			if keyS == keyB :
				if  type(Small[keyS]) != type(Big[keyB]):
                                	print("type missmatch sapadala na bhau"+str(Small[keyS])+"    "+str(Big[keyB]))
                                	ValueS=str(Small[keyS])
                                	ValueB=str(Big[keyB])
                        	else:
                                	ValueS=Small[keyS]
                                	ValueB=Big[keyB]
				if ValueS==ValueB :
			
					Count+=1
	print("length of Small = "+str(len(Small))+" unique= "+str(Count))		
	if Count == len(Small):
		print("mar tichya")		
		return True
			
	else:
		return False

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
	MatchDict={}
	CheckDict={}
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
			print(CommandList)
			print(MatchDict)
			print(CheckDict)
			for command in CommandList:
                        	for key in command:
                                	dut=key
                                        CmdList.append(command[key])
                                        openCapiOnDut( dut, capiUsername='admin', capiPassword='', capiProtocol='http', capiFormat='json' )
                                        Result=capiCmd( dut, CmdList, capiUsername='admin', capiPassword='', capiProtocol='http', capiFormat='json' )
       	                                closeCapiOnDut( dut )
			if MatchFound :
				ResultDict=Result[1]
				#print(ResultDict)
				#ResultList=[]	
				for key in ResultDict:
					ResultList=ResultDict[key]
				#print("##################")
				#print(ResultList)
				
				unique=0
				MyDict={}
				NormalResultList=[]
				for dict in ResultList:
					NormalDict={}
					for key in dict:
						#print(dict[key])
						#print(type(dict[key]))
						if type(key)== unicode: 
							NonUnicodeKey=key.encode("utf-8")
							if type(dict[key])== unicode:
								NonUnicodeValue=dict[key].encode("utf-8")
								NormalDict[NonUnicodeKey]=NonUnicodeValue
							elif type(dict[key]) == list :
                                                                print("ghavala")
                                                                NonUnicodeValueList=[]
                                                               	for l in dict[key]:
                                                                        print("sapadala na bho")
                                                                        print(l)
                                                                        print(type(l))
                                                                        if type(l) == unicode:
                                                                        	NonUnicodeValueList.append(l.encode("utf-8"))
								NonUnicodeValueTuple=tuple(NonUnicodeValueList)
                                                                NormalDict[NonUnicodeKey]=NonUnicodeValueTuple
							else:
								NormalDict[NonUnicodeKey]=dict[key]
						else:
							NormalDict[key]=dict[key]
					NormalResultList.append(NormalDict)
				print(ResultList)
				print("/////////////////")
				print(NormalResultList)
				print("++++++++++++++++++")
				
				for dict in NormalResultList:
					if CompareDict(dict, MatchDict):
						if CompareDict(dict, CheckDict):
							print("First Testcase Pass na Bhau")
				#	print(set(MatchDict.items()))
				#	print(set(dict.items()))
					#if set(MatchDict.items()).issubset(set(dict.items())):
				#	if MatchDict.items().issubset(dict.items()):
				#		unique+=1	
				#		MyDict=Dict
#				#print(unique)				
				#if unique==0 :
				#	print("The Match Parameters are not found")
				#elif unique > 1 :
				#	print("The Match Parameters are not Unique")
				#else:
				#	print("Match Found now checking the check")
				#	print(MyDict)
#	print(ResultList)				
						
#	print(Result)
	#print(CommandList)	
