# Copyright (c) 2016 Arista Networks, Inc.  All rights reserved.
# Arista Networks, Inc. Confidential and Proprietar.
i=3
Step=3
while(i < 255):   
   print("STEP::"+str(Step))
   print("Command:fm241=enable")
   print("Command:fm241=configure terminal")
   print("Command:fm241=interface ethernet 7")
   print("Command:fm241=vrrp 1 priority "+str(i))
   print("Delay:10")
   print("Command:fm241=enable")
   print("Command:fm241=show vrrp brief")
   print("Match:groupId=1")
   print("Check:state=master")
   print("Delay:5")
   print("///")
   Step+=1
   print("STEP::"+str(Step))
   print("Command:fm109=enable")
   print("Command:fm109=show vrrp brief")
   print("Match:groupId=1")
   print("Check:state=backup")
   print("Delay:5")
   print("///")
   i=i+1
   Step+=1
   print("STEP::"+str(Step))
   print("Command:fm109=enable")
   print("Command:fm109=configure terminal")
   print("Command:fm109=interface ethernet 3")
   print("Command:fm109=vrrp 1 priority "+str(i))
   print("Delay:10")
   print("Command:fm241=enable")
   print("Command:fm241=show vrrp brief")
   print("Match:groupId=1")
   print("Check:state=backup")
   print("Delay:5")
   print("///")
   Step+=1
   print("STEP::"+str(Step))
   print("Command:fm109=enable")
   print("Command:fm109=show vrrp brief")
   print("Match:groupId=1")
   print("Check:state=master")
   i=i+1
   Step+=1
   print("Delay:10")
   print("///")

