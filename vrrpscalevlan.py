# Copyright (c) 2016 Arista Networks, Inc.  All rights reserved.
# Arista Networks, Inc. Confidential and Proprietary.



i=101

while (i < 117):
   print("int vlan "+str(i))
   j=41
   while (j < 49):
      print("vrrp "+str(j)+" priority 150")
      #print("no vrrp "+str(j))
      #if j < 45:
      #   print("vrrp "+str(j)+" ip 10.0."+str(i)+"."+str(j))
      #else:
      #   print("vrrp "+str(j)+" ipv6 2001:"+str(i)+"::"+str(j))
      j=j+1
   print("exit")
   i=i+1
   
