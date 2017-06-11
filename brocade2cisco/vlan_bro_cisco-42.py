"techiweb@netbackup01:~$ nano /usr/local/bin/maint_helper.py"

#!/usr/bin/env python  

'''
Please note, Alain is not liable for an outage that you caused
after using this script :)
'''





#import ipcalc
import re
import sys
import os 
from myiweblib3 import *
import collections
#import functools

	
	# Modular variable
#interface_type = ''	
#interface_type = 'NON-VALIDE'



 	# Globale Variables


lookup_interface_ve = '^interface ve' 
interface_ve_dict = {}
gl_Vlan_List = []

hostname = ''
ipmtu = ''
access_list_out = '**'
access_list_in = '**'
vrf_on_int_ve = '**'
gl_vrf_list = []
static_routes_null = []
static_routes = []


line_int_ve_begin = []
line_int_ve_end = []
interface = False

  

number_ipv4_vrid = 0
number_ipv6_vrid = 0
number_ip_v6_addr = 0
number_ip_helper = 0
number_ip_v6 = 0
number_ip_v6_non_vrrp = 0
number_ip_v4_addr = 0


Index_Begin_Interface_Ve = 0
Index_End_Interface_Ve = 0

strtest1 = ''
actual_vlan = ''
iactual_vlan = 0


ciscoConfiguration = []
brocadeConfiguration = []
access_lists = []
access_lists_ext = []
vrf_config = []
#findvlans1 = []
#findvlans2 = []
vlanDescriptionName = ''

matches_ip =''
markerIndex = 0

source = Ftn_Read_Backup_File ()
gl_Vlan_List = Find_Configured_Interface_Vlan(source) 
gl_Vlan_List  = map(int, gl_Vlan_List )
interface_ve_dict = Generate_Interface_Ve_Dict(gl_Vlan_List)

interface_ve_dict = collections.OrderedDict(sorted(interface_ve_dict.items()))

#for key, value in od.iteritems() :
 #   print type(key), value

#print interface_ve_dict

#exit()

static_routes,static_routes_null=FindStaticRoutes(source)
#print static_routes_null
#print static_routes

for  num, line in enumerate(source , 1):
	if re.search('^vrf',line):
		vrf_config.append(line)

	if re.search('^vlan',line):
		for m in re.finditer('vlan', line):
			markerIndex = m.end()
			#print('vlan in vlan line found:', m.start(), m.end())
		for k in re.finditer('name', line):
			#print('name in vlan line found:', k.start(), k.end())
			vlanDescriptionName = line[k.end():].strip()

		#print line
		#print line[m.end()+1:k.start()-1]
		#print line[k.end():].strip()
		#findvlans1.append(line[k.end():].strip())
		#findvlans2.append(line[m.end()+1:k.start()-1].strip())

		#vlanDescriptionName = line[k.end():].strip()
		vlanID = line[m.end()+1:k.start()-1].strip()
		vlanID = line[markerIndex+1:k.start()-1].strip()
		ivlanID = (int)(vlanID)
		#print type(ivlanID)
		#exit()
		if ivlanID in gl_Vlan_List:
			(interface_ve_dict[ivlanID]['vlanName']) = vlanDescriptionName
		
		


for  num, line in enumerate(source , 1):


	
	
	if re.search('^ip access-list extended',line):
		access_lists_ext.append(line)
		#print num

	

	if re.search('^access-list',line):
		access_lists.append(line)	
		#print access_lists


	if re.search('^hostname',line):
		hostname = line.strip('hostname').strip()	
		

	if re.search(lookup_interface_ve , line):
		line_int_ve_begin.append(num)
		Index_Begin_Interface_Ve = line_int_ve_begin[-1]
		actual_vlan = str(line.strip('interface ve'))
		iactual_vlan = actual_vlan.strip('\n')
		iactual_vlan = int(actual_vlan)
		
		interface = True
		continue
	if interface:
			

		#if re.search(lookup_ipv4_address, line):
		if re.search("ip address", line):	
			number_ip_v4_addr = number_ip_v4_addr + 1 
				

		# determine how many secoondary interfaces exist per int ve. The maximum is need to plan the model
		if re.search("ip vrrp-extended vrid", line):
			number_ipv4_vrid = number_ipv4_vrid + 1

		# determine how many secoondary ipv6 interfaces exist per int ve. The maximum is need to plan the model
		if re.search("ipv6 vrrp-extended vrid", line):
			number_ipv6_vrid = number_ipv6_vrid + 1
			#max_ipv6_vrid_per_int_ve = max_ipv6_vrid_per_int_ve + 1	

		# determine how many secoondary ipv6 interfaces exist per int ve. The maximum is need to plan the model
		if re.search("ipv6 address", line):
			number_ip_v6_addr = number_ip_v6_addr + 1
				


		# determine if disable	
		if re.search("disable", line):
			(interface_ve_dict[iactual_vlan]['enable']) = 0

		# determine if port description
		test = ''
		if re.search("port-name", line):
			(interface_ve_dict[iactual_vlan]['description']) = line.replace('port-name','').strip()
			#print interface_ve_dict[actual_vlan]['description']
			#exit()

		# determine vrf
		if re.search("vrf", line):
			gl_vrf_list.append(line)
			vrf_on_int_ve =gl_vrf_list[-1]=gl_vrf_list[-1].strip('vrf forwarding').strip('\n')
			(interface_ve_dict[iactual_vlan]['vrf']) = vrf_on_int_ve
			

		# determine mtu
		if re.search("ip mtu", line):
			#print line
		 	#ipmtu =line.strip('ip mtu')
		 	(interface_ve_dict[iactual_vlan]['ip-mtu']) = line.strip('ip mtu').strip('\n')
		 	#print line.strip('ip mtu').strip('\n')
		 	#exit()
		 	

		 # determine access-list
		if re.search("access-group .+ out", line):
		 	access_list_out = line
		 	access_list_out = access_list_out.strip('\n').strip ('ip access-group').strip('out')
		 	(interface_ve_dict[iactual_vlan]['access-group-out']) = access_list_out
		 	
	
		if re.search("access-group .+ in", line):
			access_list_in = line
			access_list_in = access_list_in.strip('\n').strip ('ip access-group').strip('in')
			(interface_ve_dict[iactual_vlan]['access-group-in']) = access_list_in

						
		if line and  re.search("^!",line):
			line_int_ve_end.append(num -1)	
			interface = False
			Index_End_Interface_Ve = line_int_ve_end[-1]
			
			

			
			#FtnInterfaceVe_VRRP_FINDER(actual_vlan,line_int_ve_begin[-1],Index_Begin_Interface_Ve,Index_End_Interface_Ve,number_ipv4_vrid,number_ipv6_vrid,number_ip_v4_addr,number_ip_v6_addr,vrf_on_int_ve,access_list_in,access_list_out,ipmtu,interface_ve_dict[actual_vlan])
			FtnInterfaceVe_VRRP_FINDER(source,iactual_vlan,line_int_ve_begin[-1],Index_Begin_Interface_Ve,Index_End_Interface_Ve,number_ipv4_vrid,number_ipv6_vrid,number_ip_v4_addr,number_ip_v6_addr,vrf_on_int_ve,access_list_in,access_list_out,ipmtu,interface_ve_dict)
				
			iactual_vlan = 0	
			actual_vlan = '0'	
			access_list_in = '**' 
			access_list_out = '**'
			vrf_on_int_ve = '**'
			number_ip_v4_addr = 0
			max_ip_v4_per_int_ve = 0
			number_ipv4_vrid = 0
			number_ipv6_vrid = 0
			number_ip_v6_addr  = 0
			vlanDescriptionName = ''
			
		
			
			

print('%10s' % ('\n END_FOR_LOOP \n'))

#print access_lists



#interface_type = 'V4_VRRP'
#ciscoConfiguration = GenerateCiscoConfig(interface_type,interface_ve_dict)


interface_type = 'NON-VALIDE'
filenamePrefix = 'cisco_config_file_'
filenamePrefix_bro = 'brocade_config_file_'
filenameSuffix = hostname + '_' + interface_type
brocadeConfiguration = GenerateBrocadeConfig(interface_type,interface_ve_dict)
filecreation('brocade',hostname,filenamePrefix_bro,filenameSuffix,brocadeConfiguration,interface_ve_dict)



interface_type = 'V4_VRRP'
filenamePrefix = 'cisco_config_file_'
filenamePrefix_bro = 'brocade_config_file_'
filenameSuffix = hostname + '_' + interface_type
#filenameSuffix = hostname + 'V4_VRRP_NEW'
ciscoConfiguration = GenerateCiscoConfig(interface_type,interface_ve_dict,hostname)
brocadeConfiguration = GenerateBrocadeConfig(interface_type,interface_ve_dict)
filecreation('cisco',hostname,filenamePrefix,filenameSuffix,ciscoConfiguration,interface_ve_dict)
filecreation('brocade',hostname,filenamePrefix_bro,filenameSuffix,brocadeConfiguration,interface_ve_dict)



interface_type = 'V4_MIXTE'
filenamePrefix = 'cisco_config_file_'
filenamePrefix_bro = 'brocade_config_file_'
filenameSuffix = hostname + '_' + interface_type
ciscoConfiguration = GenerateCiscoConfig(interface_type,interface_ve_dict,hostname)
filecreation('cisco',hostname,filenamePrefix,filenameSuffix,ciscoConfiguration,interface_ve_dict)
filecreation('brocade',hostname,filenamePrefix_bro,filenameSuffix,brocadeConfiguration,interface_ve_dict)

interface_type = 'V4_NON-VRRP'
filenamePrefix = 'cisco_config_file_'
filenamePrefix_bro = 'brocade_config_file_'
filenameSuffix = hostname + '_' + interface_type
ciscoConfiguration = GenerateCiscoConfig(interface_type,interface_ve_dict,hostname)
filecreation('cisco',hostname,filenamePrefix,filenameSuffix,ciscoConfiguration,interface_ve_dict)
filecreation('brocade',hostname,filenamePrefix_bro,filenameSuffix,brocadeConfiguration,interface_ve_dict)

'''
subnetManagement(interface_ve_dict)
#print static_routes
for x in ipcalc.Network('172.28.5.33/27'):
	print str(x)

ip_calculate('192.170.158.217/29')
addressInNetwork("107.6.122.139","107.6.122.128/27")

'''

nonvalid_Ve = []
vrrp_full_Ve = []
non_vrrp_Ve = []
vrrp_mixte_Ve = []

nonvalid_Ve,vrrp_full_Ve,non_vrrp_Ve,vrrp_mixte_Ve = FindStats(interface_ve_dict)
#print static_routes
#print static_routes_null
#print access_lists_ext
#print nonvalid_Ve
print '*****************************'	
print '****static routes***'
for item in range(len(static_routes)):
	print static_routes[item].strip()

print '*****************************'	
print '***null routes***'
for item in range(len(static_routes_null)):
	print static_routes_null[item].strip()	

print '*****************************'	
print '***standard access lists***'
for item in range(len(access_lists)):
	print access_lists[item].strip()	

print '*****************************'	
print '***standard access lists_ext***'
for item in range(len(access_lists_ext)):
	print access_lists_ext[item].strip()

print '*****************************'	
print '***vrf***'
for item in range(len(vrf_config)):
	print vrf_config[item].strip()		

print '*****************************'	
print '***STATS***'	

print hostname
print('total_non_valide_int_ve: %14s' % len(nonvalid_Ve))
print('total_full_vrrp_int_ve: %15s' % len(vrrp_full_Ve))
print('total_non_vrrp_int_ve: %16s' % len(non_vrrp_Ve))
print('total_vrrp_mixte_int_ve: %14s' % len(vrrp_mixte_Ve))
print('total_int_ve: %15s' % len(line_int_ve_begin))
#print len(nonvalid_Ve) + len(vrrp_full_Ve) + len(non_vrrp_Ve) + len(vrrp_mixte_Ve)
#print interface_ve_dict['2286']








	