  


import os
import sys
import select
import re
import time

	


################################
def Ftn_Read_File ():
	source = ''
	conf1 = ' '
	if len(sys.argv) >= 2:
		try:
				conf1 = sys.argv[-1]
				
				
				 
		except:
				print 'Something is wrong with your arguments. \
					   Please reference help.'

	else:   
		print 'No arguments was provided. Please use \
						"a file to run the script".'   

	# read the config file
	try:
		with open(conf1) as f:
				source = f.readlines()


	except IOError:
		print "Can't read running config file."
	
	return (source)

############################
'''

def Ftn_Read_File2():
	if len(sys.argv) > 1:
		try:
			conf1 = sys.argv[-4]
			conf2 = sys.argv[-3]
			conf3 = sys.argv[-2]
			conf4 = sys.argv[-1]
			
		except:
			print 'Something is wrong with your arguments. \
Please reference help.'
	else:
		print 'No arguments was provided. Please use \
"./maint_helper source_running_file destination_running_file".'
      
	try:
		with open(conf1) as f:
			oldvlans = f.readlines()
		with open(conf2) as f:
			newvlans = f.readlines()
		with open(conf3) as f:
			newvprids = f.readlines()
		with open(conf4) as f:
			newips = f.readlines()	
				
	except IOError:
		print "Can't read running config file."

	return oldvlans,newvlans,newvprids,newips

	'''
		

##########################

def Format_File_Input_To_Array():
	Array = []
	source = Ftn_Read_File ()
	for  num, line in enumerate(source , 0):
		if len(line) != 0:
			Array.append(line)
	return Array


def Format_File_Input_To_Array2():
	Arrayold = []
	Arraynew = []
	Arrayvprids =[]
	Arrayips = []
	oldvlans,newvlans,Newvprids,NewIps = Ftn_Read_File2()
	
	for  num, line in enumerate(oldvlans , 0):
		if len(line) != 0:
			Arrayold.append(line)

	for  num, line in enumerate(newvlans , 0):
		if len(line) != 0:
			Arraynew.append(line)	

	for  num, line in enumerate(Newvprids , 0):
		if len(line) != 0:
			Arrayvprids.append(line)

	for  num, line in enumerate(NewIps , 0):
		if len(line) != 0:
			Arrayips.append(line)		
						
	return Arrayold,Arraynew,Arrayvprids,Arrayips	



oldarrayvlans = []
newarrayvlans = []
newarrayvprids = []
newarrayips = []
vlanLAN = 0

#print newarrayips
#print newarrayvprids
vlan = 0
source = Ftn_Read_File()

#oldarrayvlans,newarrayvlans,newarrayvprids,newarrayips = Format_File_Input_To_Array2()


for  num, line in enumerate(source , 1):

	if re.search('^@oldvlan',line):
		vlan = line.strip('@oldvlan').strip()
		oldarrayvlans.append(vlan)

	if re.search('^@newvlan',line):
		vlan = line.strip('@newvlan').strip()
		newarrayvlans.append(vlan)	

	if re.search('^@newvprid',line):
		vlan = line.strip('@newvprid').strip()
		newarrayvprids.append(vlan)	

	if re.search('^@newip',line):
		vlan = line.strip('@newip').strip()
		newarrayips.append(vlan)		

print oldarrayvlans
print newarrayvlans
print newarrayvprids
print newarrayips
#exit()		




print '****************************************'
print '****************************************'
print '***config for 903-01SH****'
print '****************************************'
for vlans in range(len(oldarrayvlans)):
	print('delete protocols vstp vlan %s' % oldarrayvlans[vlans].strip())
	print('delete vlans VLAN%s' % oldarrayvlans[vlans].strip())
	print('delete interfaces ae0 unit 0 family ethernet-switching vlan members %s' % oldarrayvlans[vlans].strip())
	print('delete interfaces ae1 unit 0 family ethernet-switching vlan members %s' % oldarrayvlans[vlans].strip())
	print('delete interfaces ae2 unit 0 family ethernet-switching vlan members %s' % oldarrayvlans[vlans].strip())
print '****************************************'
print '****************************************'
print '***config for 903-01SH****New VPR'
print '****************************************'
for vlans in range(len(newarrayvlans)):
	print('set vlans VLAN%s description VPR-%s-WAN' % (newarrayvlans[vlans].strip(),newarrayvprids[vlans].strip()))	
	print('set vlans VLAN%s vlan-id %s ' % (newarrayvlans[vlans].strip(),newarrayvlans[vlans].strip()))
	print('set interfaces ae0 unit 0 family ethernet-switching vlan members  %s' % newarrayvlans[vlans].strip())
	print('set interfaces ae1 unit 0 family ethernet-switching vlan members  %s' % newarrayvlans[vlans].strip())
	print('set interfaces ae2 unit 0 family ethernet-switching vlan members  %s' % newarrayvlans[vlans].strip())
	print('set protocols vstp vlan %s bridge-priority 0 ' % newarrayvlans[vlans].strip())

print '****************************************'
print '****************************************'
print '***config for 903-02SH****New VPR'
print '****************************************'
for vlans in range(len(newarrayvlans)):
	vlanLAN = (int)(newarrayvlans[vlans].strip())
	vlanLAN = vlanLAN + 1


	print('set vlans VLAN%s description VPR-%s-WAN' % (newarrayvlans[vlans].strip(),newarrayvprids[vlans].strip()))	
	print('set vlans VLAN%s vlan-id  %s ' % (newarrayvlans[vlans].strip(),newarrayvlans[vlans].strip()))

	print('set vlans VLAN%s description VPR-%s-LAN' % (vlanLAN,newarrayvprids[vlans].strip()))		
	print('set vlans VLAN%s vlan-id  %s ' % (vlanLAN,vlanLAN))

vlanLAN = (int)(newarrayvlans[-1].strip())
vlanLAN = vlanLAN + 1
print('set interfaces ae0 unit 0 family ethernet-switching vlan members %s-%s' % (newarrayvlans[0].strip(),vlanLAN))
print('set interfaces ae1 unit 0 family ethernet-switching vlan members %s-%s' % (newarrayvlans[0].strip(),vlanLAN))
print('set interfaces ae11 unit 0 family ethernet-switching vlan members %s-%s' % (newarrayvlans[0].strip(),vlanLAN))
print('set interfaces ae12 unit 0 family ethernet-switching vlan members %s-%s' % (newarrayvlans[0].strip(),vlanLAN))
print('set interfaces ae13 unit 0 family ethernet-switching vlan members %s-%s' % (newarrayvlans[0].strip(),vlanLAN))
print('set interfaces ae14 unit 0 family ethernet-switching vlan members %s-%s' % (newarrayvlans[0].strip(),vlanLAN))
print('set interfaces ae15 unit 0 family ethernet-switching vlan members %s-%s' % (newarrayvlans[0].strip(),vlanLAN))
print('set interfaces ae16 unit 0 family ethernet-switching vlan members %s-%s' % (newarrayvlans[0].strip(),vlanLAN))
print('set interfaces ae17 unit 0 family ethernet-switching vlan members %s-%s' % (newarrayvlans[0].strip(),vlanLAN))
print('set interfaces ae18 unit 0 family ethernet-switching vlan members %s-%s' % (newarrayvlans[0].strip(),vlanLAN))
print('set interfaces ae19 unit 0 family ethernet-switching vlan members %s-%s' % (newarrayvlans[0].strip(),vlanLAN))
print('set interfaces ae20 unit 0 family ethernet-switching vlan members %s-%s' % (newarrayvlans[0].strip(),vlanLAN))
print('set interfaces ae21 unit 0 family ethernet-switching vlan members %s-%s' % (newarrayvlans[0].strip(),vlanLAN))
print('set interfaces ae22 unit 0 family ethernet-switching vlan members %s-%s' % (newarrayvlans[0].strip(),vlanLAN))
print('set interfaces ae23 unit 0 family ethernet-switching vlan members %s-%s' % (newarrayvlans[0].strip(),vlanLAN))
print('set interfaces ae24 unit 0 family ethernet-switching vlan members %s-%s' % (newarrayvlans[0].strip(),vlanLAN))
print('set interfaces ae25 unit 0 family ethernet-switching vlan members %s-%s' % (newarrayvlans[0].strip(),vlanLAN))
print('set interfaces ae26 unit 0 family ethernet-switching vlan members %s-%s' % (newarrayvlans[0].strip(),vlanLAN))
print('set interfaces ae27 unit 0 family ethernet-switching vlan members %s-%s' % (newarrayvlans[0].strip(),vlanLAN))
print('set interfaces ae28 unit 0 family ethernet-switching vlan members %s-%s' % (newarrayvlans[0].strip(),vlanLAN))
print('set interfaces ae29 unit 0 family ethernet-switching vlan members %s-%s' % (newarrayvlans[0].strip(),vlanLAN))
print('set interfaces ae30 unit 0 family ethernet-switching vlan members %s-%s' % (newarrayvlans[0].strip(),vlanLAN))

print('set interfaces ae31 unit 0 family ethernet-switching vlan members %s-%s' % (newarrayvlans[0].strip(),vlanLAN))
print('set interfaces ae32 unit 0 family ethernet-switching vlan members %s-%s' % (newarrayvlans[0].strip(),vlanLAN))
print('set interfaces ae33 unit 0 family ethernet-switching vlan members %s-%s' % (newarrayvlans[0].strip(),vlanLAN))
print('set interfaces ae34 unit 0 family ethernet-switching vlan members %s-%s' % (newarrayvlans[0].strip(),vlanLAN))
print('set interfaces ae35 unit 0 family ethernet-switching vlan members %s-%s' % (newarrayvlans[0].strip(),vlanLAN))
print('set interfaces ae36 unit 0 family ethernet-switching vlan members %s-%s' % (newarrayvlans[0].strip(),vlanLAN))
print('set interfaces ae37 unit 0 family ethernet-switching vlan members %s-%s' % (newarrayvlans[0].strip(),vlanLAN))
print('set interfaces ae38 unit 0 family ethernet-switching vlan members %s-%s' % (newarrayvlans[0].strip(),vlanLAN))
print('set interfaces ae39 unit 0 family ethernet-switching vlan members %s-%s' % (newarrayvlans[0].strip(),vlanLAN))
print('set interfaces ae40 unit 0 family ethernet-switching vlan members %s-%s' % (newarrayvlans[0].strip(),vlanLAN))

print('set interfaces ae51 unit 0 family ethernet-switching vlan members %s-%s' % (newarrayvlans[0].strip(),vlanLAN))
print('set interfaces ae52 unit 0 family ethernet-switching vlan members %s-%s' % (newarrayvlans[0].strip(),vlanLAN))
print('set interfaces ae53 unit 0 family ethernet-switching vlan members %s-%s' % (newarrayvlans[0].strip(),vlanLAN))
print('set interfaces ae54 unit 0 family ethernet-switching vlan members %s-%s' % (newarrayvlans[0].strip(),vlanLAN))
print('set interfaces ae55 unit 0 family ethernet-switching vlan members %s-%s' % (newarrayvlans[0].strip(),vlanLAN))
print('set interfaces ae56 unit 0 family ethernet-switching vlan members %s-%s' % (newarrayvlans[0].strip(),vlanLAN))
print('set interfaces ae57 unit 0 family ethernet-switching vlan members %s-%s' % (newarrayvlans[0].strip(),vlanLAN))
print('set interfaces ae58 unit 0 family ethernet-switching vlan members %s-%s' % (newarrayvlans[0].strip(),vlanLAN))
print('set interfaces ae59 unit 0 family ethernet-switching vlan members %s-%s' % (newarrayvlans[0].strip(),vlanLAN))
print('set interfaces ae60 unit 0 family ethernet-switching vlan members %s-%s' % (newarrayvlans[0].strip(),vlanLAN))

print('set interfaces ae61 unit 0 family ethernet-switching vlan members %s-%s' % (newarrayvlans[0].strip(),vlanLAN))
print('set interfaces ae62 unit 0 family ethernet-switching vlan members %s-%s' % (newarrayvlans[0].strip(),vlanLAN))
print('set interfaces ae63 unit 0 family ethernet-switching vlan members %s-%s' % (newarrayvlans[0].strip(),vlanLAN))
print('set interfaces ae64 unit 0 family ethernet-switching vlan members %s-%s' % (newarrayvlans[0].strip(),vlanLAN))
print('set interfaces ae65 unit 0 family ethernet-switching vlan members %s-%s' % (newarrayvlans[0].strip(),vlanLAN))
print('set interfaces ae66 unit 0 family ethernet-switching vlan members %s-%s' % (newarrayvlans[0].strip(),vlanLAN))
print('set interfaces ae67 unit 0 family ethernet-switching vlan members %s-%s' % (newarrayvlans[0].strip(),vlanLAN))
print('set interfaces ae68 unit 0 family ethernet-switching vlan members %s-%s' % (newarrayvlans[0].strip(),vlanLAN))
print('set interfaces ae69 unit 0 family ethernet-switching vlan members %s-%s' % (newarrayvlans[0].strip(),vlanLAN))
print('set interfaces ae70 unit 0 family ethernet-switching vlan members %s-%s' % (newarrayvlans[0].strip(),vlanLAN))

print('set interfaces ae71 unit 0 family ethernet-switching vlan members %s-%s' % (newarrayvlans[0].strip(),vlanLAN))
print('set interfaces ae72 unit 0 family ethernet-switching vlan members %s-%s' % (newarrayvlans[0].strip(),vlanLAN))
print('set interfaces ae73 unit 0 family ethernet-switching vlan members %s-%s' % (newarrayvlans[0].strip(),vlanLAN))
print('set interfaces ae74 unit 0 family ethernet-switching vlan members %s-%s' % (newarrayvlans[0].strip(),vlanLAN))
print('set interfaces ae75 unit 0 family ethernet-switching vlan members %s-%s' % (newarrayvlans[0].strip(),vlanLAN))
print('set interfaces ae76 unit 0 family ethernet-switching vlan members %s-%s' % (newarrayvlans[0].strip(),vlanLAN))
print('set interfaces ae77 unit 0 family ethernet-switching vlan members %s-%s' % (newarrayvlans[0].strip(),vlanLAN))
print('set interfaces ae78 unit 0 family ethernet-switching vlan members %s-%s' % (newarrayvlans[0].strip(),vlanLAN))
print('set interfaces ae79 unit 0 family ethernet-switching vlan members %s-%s' % (newarrayvlans[0].strip(),vlanLAN))
print('set interfaces ae80 unit 0 family ethernet-switching vlan members %s-%s' % (newarrayvlans[0].strip(),vlanLAN))

print('set interfaces ae81 unit 0 family ethernet-switching vlan members %s-%s' % (newarrayvlans[0].strip(),vlanLAN))
print('set interfaces ae82 unit 0 family ethernet-switching vlan members %s-%s' % (newarrayvlans[0].strip(),vlanLAN))
print('set interfaces ae83 unit 0 family ethernet-switching vlan members %s-%s' % (newarrayvlans[0].strip(),vlanLAN))
print('set interfaces ae84 unit 0 family ethernet-switching vlan members %s-%s' % (newarrayvlans[0].strip(),vlanLAN))
print('set interfaces ae85 unit 0 family ethernet-switching vlan members %s-%s' % (newarrayvlans[0].strip(),vlanLAN))
print('set interfaces ae86 unit 0 family ethernet-switching vlan members %s-%s' % (newarrayvlans[0].strip(),vlanLAN))
print('set interfaces ae87 unit 0 family ethernet-switching vlan members %s-%s' % (newarrayvlans[0].strip(),vlanLAN))
print('set interfaces ae88 unit 0 family ethernet-switching vlan members %s-%s' % (newarrayvlans[0].strip(),vlanLAN))
print('set interfaces ae89 unit 0 family ethernet-switching vlan members %s-%s' % (newarrayvlans[0].strip(),vlanLAN))	
		
print '****************************************'
print '****************************************'
print '***config for DR11****New VPR'
print '****************************************'

print '****************************************'
print '****************************************'
print '******DR11 config******'
print '****************************************'
counter = 0
count1 = 0
count2 = 0
vlancounter =0



for vlans in range(len(newarrayvlans)):
	print('vlan %s' %newarrayvlans[vlans].strip())
	print('name VPR-%s-WAN' % newarrayvprids[vlans].strip())
	print('exit')

	
print '****************************************'

print ('interface Po201')
for vlans in range(len(newarrayvlans)):
	print ('switchport trunk allowed vlan add %s' %newarrayvlans[vlans].strip())	

print '****************************************'	

for ips in range(len(newarrayips)):
	
	if not(ips % 4):

		#print 'find'
		#print ips
		counter = ips
		if (counter +2) < (len(newarrayips) - 1):
			count1 = counter + 1
			count2 = count1 + 1
			#print 'counter %d' %counter
			#print 'count1 %d' %count1
			#print 'count2 %d' %count2
		
			print('interface vlan %s' % (newarrayvlans[vlancounter].strip()))
			print('description VPR-%s-WAN | %s | %s | %s | Vlan%s ' % (newarrayvprids[vlancounter].strip(),newarrayips[counter].strip(),newarrayips[count1].strip(),newarrayips[count2].strip(),newarrayvlans[vlancounter].strip()))
			print('ip address %s 255.255.255.224 ' % (newarrayips[count2].strip()))
			print('ip verify unicast source reachable-via rx ')
			print('no ip redirects')
			print('no ip proxy-arp')
			print('standby 1 ip %s' % (newarrayips[count1].strip()))
			print('standby 1 timers 5 15')
			print('standby 1 priority 110')
			print('standby 1 preempt delay minimum 60')
			print('standby 1 authentication VLAN%s' % (newarrayvlans[vlancounter].strip()))
			print('standby 1 track 101 decrement 50')
			print('service-policy input 1GbpsLimit')
			print('service-policy output 1GbpsLimit')
			print('no shut')
			print('exit')
			count1 = 0
			count2 = 0
			vlancounter = vlancounter + 1
	#else:
		#print 'not find'
		#print ips

print '****************************************'
print '****************************************'
print '******DR12 config******'
print '****************************************'
counter = 0
count1 = 0
count2 = 0
vlancounter =0

for ips in range(len(newarrayips)):
	
	if not(ips % 4):

		#print 'find'
		#print ips
		counter = ips
		if (counter +2) < (len(newarrayips) - 1):
			count1 = counter + 1
			count2 = count1 + 2
			#print 'counter %d' %counter
			#print 'count1 %d' %count1
			#print 'count2 %d' %count2
			#print 'vlanconter %d' %vlancounter
		
			print('interface vlan %s' % (newarrayvlans[vlancounter].strip()))
			print('description VPR-%s-WAN | %s | %s | %s | Vlan%s ' % (newarrayvprids[vlancounter].strip(),newarrayips[counter].strip(),newarrayips[count1].strip(),newarrayips[count2].strip(),newarrayvlans[vlancounter].strip()))
			print('ip address %s 255.255.255.224 ' % (newarrayips[count2].strip()))
			print('ip verify unicast source reachable-via rx ')
			print('no ip redirects')
			print('no ip proxy-arp')
			print('standby 1 ip %s' % (newarrayips[count1].strip()))
			print('standby 1 timers 5 15')
			print('standby 1 priority 90')
			print('standby 1 preempt delay minimum 60')
			print('standby 1 authentication VLAN%s' % (newarrayvlans[vlancounter].strip()))
			print('standby 1 track 101 decrement 50')
			print('service-policy input 1GbpsLimit')
			print('service-policy output 1GbpsLimit')
			print('no shut')
			print('exit')
			count1 = 0
			count2 = 0
			vlancounter = vlancounter + 1
	#else:
		#print 'not find'
		#print ips


		
 
 
 

 
 
 
		
		
	




