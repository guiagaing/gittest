
import sys
import os
import re
import socket,struct
#from netaddr import IPNetwork, IPAddress


####################################
def addressInNetwork(ip,net):
	if IPAddress(ip) in IPNetwork(net):
		print "Yay!"



######################################


def FindStaticRoutes(originalfile):
	static_routes = []
	static_routes_null = []

	for  num, line in enumerate(originalfile , 1):
		if re.search('^ip route',line):
			if re.search('null0',line):
				for m in re.finditer('\d+\.\d+\.\d+\.\d+/\d\d', line):
					#print('ip address found:', m.start(), m.end()),len(line)
					#print line[m.start():m.end()]
					#print line[(m.end())-2:m.end()]
					#print calcDottedNetmask((int)(line[(m.end())-2:m.end()])
					#print line[m.end():]
					#static_routes_null.append(line[m.start():m.end()])
					#print 'ip route ' + line[m.start():(m.end() -3)] + ' ' + calcDottedNetmask((int)(line[(m.end())-2:m.end()])) + '' + line[m.end():]
					print 'ip route ' + line[m.start():(m.end() -3)] + ' ' + calcDottedNetmask((int)(line[(m.end())-2:m.end()])) + ' ' + 'null0'
					static_routes_null.append('ip route ' + line[m.start():(m.end() -3)] + ' ' + calcDottedNetmask((int)(line[(m.end())-2:m.end()])) + ' ' + 'null0')
			else:
				for m in re.finditer('\d+\.\d+\.\d+\.\d+/\d\d', line):
					#print('ip address found:', m.start(), m.end()),len(line)
					#print line[m.start():m.end()]
					#print line[(m.end())-2:m.end()]
					#print calcDottedNetmask((int)(line[(m.end())-2:m.end()]))
					#print line[m.end():]
					#static_routes.append(line[m.start():m.end()])
					print 'ip route ' + line[m.start():(m.end() -3)] + ' ' + calcDottedNetmask((int)(line[(m.end())-2:m.end()])) + '' + line[m.end():]
					static_routes.append('ip route ' + line[m.start():(m.end() -3)] + ' ' + calcDottedNetmask((int)(line[(m.end())-2:m.end()])) + '' + line[m.end():])

					#print static_routes_null
					#print static_routes	

	return static_routes,static_routes_null




	




################################################

def _dec_to_binary(ip_address):
    return map(lambda x: bin(x)[2:].zfill(8), ip_address)


def _negation_mask(net_mask):
    wild = list()
    for i in net_mask:
        wild.append(255 - int(i))
    return wild

def ip_calculate(ip):
	ip = IPCalculator(ip)
 	ip.__repr__()


class IPCalculator(object):
    def __init__(self, ip_address, cdir=24):
        if '/' in ip_address:
            self._address_val, self._cidr = ip_address.split('/')
            self._address = map(int, self._address_val.split('.'))
        else:
            self._address = map(int, ip_address.split('.'))
            self._cidr = cdir
        self.binary_IP = _dec_to_binary(self._address)
        self.binary_Mask = None
        self.negation_Mask = None
        self.network = None
        self.broadcast = None

    def __repr__(self):
        print "Calculating the IP range of %s/%s" % (".".join(map(str, self._address)), self._cidr)
        print "=================================="
        print "Netmask %s" % (".".join(map(str, self.net_mask())))
        print "Network ID %s" % (".".join(map(str, self.network_ip())))
        print "Subnet Broadcast address %s" % (".".join(map(str, self.broadcast_ip())))
        print "Host range %s" % (self.host_range())
        print "Max number of hosts %s" % (self.number_of_host())

    def net_mask(self):
        mask = [0, 0, 0, 0]
        for i in range(int(self._cidr)):
            mask[i / 8] += 1 << (7 - i % 8)
        self.binary_Mask = _dec_to_binary(mask)
        self.negation_Mask = _dec_to_binary(_negation_mask(mask))
        return mask

    def broadcast_ip(self):
        broadcast = list()
        for x, y in zip(self.binary_IP, self.negation_Mask):
            broadcast.append(int(x, 2) | int(y, 2))
        self.broadcast = broadcast
        return broadcast

    def network_ip(self):
        network = list()
        for x, y in zip(self.binary_IP, self.binary_Mask):
            network.append(int(x, 2) & int(y, 2))
        self.network = network
        return network

    def host_range(self):
        min_range = self.network
        min_range[-1] += 1
        max_range = self.broadcast
        max_range[-1] -= 1
        return "%s - %s" % (".".join(map(str, min_range)), ".".join(map(str, max_range)))

    def number_of_host(self):
        return (2 ** sum(map(lambda x: sum(c == '1' for c in x), self.negation_Mask))) - 2



#########################################################################
#Subnet and IPs management
def subnetManagement(InteVeModel):
	subnets = []
	vlans = []
	for k,v in InteVeModel.iteritems():
		if InteVeModel[k]['ve_type_v4'] != 'NON-VALIDE':
			subnets.append(InteVeModel[k]['ipv4'])
			vlans.append(k)

	#print (subnets)
	#print (vlans)		
		


	return


def filecreation(deviceType,hostname, filenamePrefix,filenameSuffix,config):
    #print "alist"
    line = ''
    vlan = ''
    filename = filenamePrefix + filenameSuffix
    
    with open(filename, 'w') as d:
    	d.writelines(hostname)
    	d.writelines('\n')
    	d.writelines('\n')
    	

    	if deviceType == 'cisco':

    		for item in range (len(config)):
    			for k in range(len(config[item])):
    				line = config[item][k]
        			if re.search('^interface',line):
        				vlan = line.strip('interface').strip()
        				d.write(vlan + '\n')
        				d.write('exit' + '\n')
        			
# write interface vlan to file
        	for item in range (len(config)):
        		for k in range(len(config[item])):
        			print config[item][k]
        			d.write(config[item][k] + '\n')


    	if deviceType == 'brocade':
    		for item in range (len(config)):
    			d.write(config[item])



	d.close()


	return


#####################################################################################	
	
'''
def GenerateReportFromBackupsToFile(InteVeModel):

	f = open ('/Users/akamdem/Documents/backups_report_file','w')
	ciscoInterface = []
	
	for k,v in InteVeModel.iteritems():
		#if InteVeModel[k]['ve_type_v4'] != 'NON-VALIDE':
		if InteVeModel[k]['ve_type_v4'] == 'V4_VRRP':
			ciscoInterface.append((PrepareCiscoInterfaceVe(k,InteVeModel[k])))	
			
	return ciscoInterface
'''	


###########################################

def Ftn_Read_Backup_File ():
	source = ''
	if len(sys.argv) >= 2:
		try:
				conf1=sys.argv[-1]
				print('%10s' % (conf1,))
				 
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

##############################################################

def Find_Configured_Interface_Vlan(source):
	vlan_list = []
	lookup_interface_ve = '^interface ve' 
	for  num, line in enumerate(source , 1):
		if re.search(lookup_interface_ve , line):
			vlan_list.append((line.strip('interface ve')).strip())
	return(vlan_list)	

############################################################

def calcDottedNetmask(mask):
	bits = 0
	from socket import inet_ntoa
	from struct import pack
	bits = 0xffffffff ^ (1 << 32 - mask) - 1
	return inet_ntoa(pack('>I', bits))	


###########################################################

def Generate_Interface_Ve_Dict(vlan_list):

	inter_ve_dict = {}
	for vlan in vlan_list:
		inter_ve_dict.update({vlan:{"ipv4":[], "ipv6":[],"vip-v4":[],"vip-v6":[],"ip-helper":[],"mtu": '-', "ip-mtu": '-', "vrf": '',"access-group-in": '',"access-group-out": '',"ve_type_v4": '-',"ve_type_v6":'-',"enable":1}})
	return inter_ve_dict

#########################################################

def PrepareCiscoInterfaceVe(vlan,brocadeInterfaceVe):
	nbreIpv4 = 0
	nbreIpv6 = 0
	nbreVipV4 = 0
	nbreVipV6 = 0
	nbreIpHelper = 0

	ciscoInterface = []
	local_dump_var =''
	len_mtu = 0
	ipv4_mtu = ''
	i = 0
	k = 0
	matches_mask = ''
	matches_ip = ''
	mask = 0
	mask_v6 = ''
	standbygroup = 1
	temp_val = 0
	#print brocadeInterfaceVe['ip-mtu']

	if brocadeInterfaceVe['ve_type_v4'] != 'NON-VALIDE':
			nbreIpv4 = len(brocadeInterfaceVe['ipv4'])
			nbreVipV4 = len(brocadeInterfaceVe['vip-v4'])
			nbreIpv6 = len(brocadeInterfaceVe['ipv6'])
			nbreVipV6 = len(brocadeInterfaceVe['vip-v6'])
			nbreIpHelper = len(brocadeInterfaceVe['ip-helper'])
			
			


	
	if brocadeInterfaceVe['ve_type_v4'] != 'NON-VALIDE':
		ciscoInterface.append('interface vlan' + ' ' + vlan )
		if len(brocadeInterfaceVe['vrf']) != 0:
			ciscoInterface.append('ip vrf forwarding ' + '' + brocadeInterfaceVe['vrf'])

# V4 Auswertung			

		if (brocadeInterfaceVe['ip-mtu']) != '-':
			ciscoInterface.append('mtu ' + ' ' + brocadeInterfaceVe['ip-mtu'])	
			
		

		for i in range(nbreIpv4):
			local_dump_var = brocadeInterfaceVe['ipv4'][i]
			matches_ip = re.findall('\d+\.\d+\.\d+\.\d+', local_dump_var)
			matches_mask = re.findall('/\d\d', local_dump_var)
			matches_mask = int(matches_mask[0].strip('/'))
			mask = calcDottedNetmask(matches_mask)
			if(i == 0):
				ciscoInterface.append('ip address ' + matches_ip[0] + ' '+ mask)

			else:
				ciscoInterface.append('ip address ' + matches_ip[0] + ' '+ mask +' '+'secondary')

		for k in range(nbreIpHelper):
			if(nbreIpHelper != 0):
				ciscoInterface.append('ip helper-address ' + '' + brocadeInterfaceVe['ip-helper'][k])

		ciscoInterface.append('ip verify unicast source reachable-via rx')	
		ciscoInterface.append('no ip redirects')	
		ciscoInterface.append('no ip proxy-arp')

		if len(brocadeInterfaceVe['access-group-in']) != 0:
			ciscoInterface.append('ip access-group ' + '' + brocadeInterfaceVe['access-group-in'] + '' + 'in')

		if len(brocadeInterfaceVe['access-group-out']) != 0:
			ciscoInterface.append('ip access-group ' + '' + brocadeInterfaceVe['access-group-out'] + '' + 'out')


		for k in range(nbreVipV4):	
			if((nbreVipV4 != 0) and ( k == 0)):
				ciscoInterface.append('standby ' + str(standbygroup) + brocadeInterfaceVe['vip-v4'][k])
				ciscoInterface.append('standby ' + str(standbygroup) +' ' + 'timers 5 15')
				ciscoInterface.append('standby ' + str(standbygroup) +' ' + 'priority 110')
				ciscoInterface.append('standby ' + str(standbygroup) +' ' + 'preempt delay minimum 60')
				ciscoInterface.append('standby ' + str(standbygroup) +' ' + 'authentication VLAN' + vlan)
				ciscoInterface.append('standby ' + str(standbygroup) +' ' + 'track 101 decrement 50')

			if((nbreVipV4 != 0) and ( k >= 1)):
				ciscoInterface.append('standby ' + str(standbygroup) + brocadeInterfaceVe['vip-v4'][k] +' '+'secondary')

		# V6 auswertung		

	if ((brocadeInterfaceVe['ve_type_v6'] != '-') and (nbreIpv6 >= 1)):
		for i in range(nbreIpv6):
			
			
			if i == 0:
				local_dump_var = brocadeInterfaceVe['ipv6'][i]
				matches_mask = re.search("/", local_dump_var)
				mask_v6 = local_dump_var[matches_mask.start():]
				ciscoInterface.append('ipv6 address ' + local_dump_var )
			else:
				local_dump_var = brocadeInterfaceVe['ipv6'][i]
				matches_mask = re.search("/", local_dump_var)
				mask_v6 = local_dump_var[matches_mask.start():]
				ciscoInterface.append('ipv6 address ' + local_dump_var +' '+'secondary')

				

			if (nbreVipV6 >= 1):
				for vip in range(nbreVipV6):
					if vip == 0:
						local_dump_var = brocadeInterfaceVe['vip-v6'][vip]
						ciscoInterface.append('standby '  + str(standbygroup)+ ' ' +'ipv6' +' '+ brocadeInterfaceVe['vip-v6'][vip] + mask_v6)
					else:
						local_dump_var = brocadeInterfaceVe['vip-v6'][vip]
						ciscoInterface.append('standby ' + str(standbygroup) + ' ' +'ipv6' +' '+ brocadeInterfaceVe['vip-v6'][vip] + mask_v6 +' '+'secondary')
			
		
	ciscoInterface.append('no shutdown')
	ciscoInterface.append('exit')
	ciscoInterface.append('\n')
	return ciscoInterface

#####################################################################################		

def GenerateCiscoConfig(ve_type,InteVeModel):


	i = 0
	ciscoInterface = []
	
	for k,v in InteVeModel.iteritems():
		#if InteVeModel[k]['ve_type_v4'] == 'NON-VALIDE':
		if InteVeModel[k]['ve_type_v4'] == ve_type:	
			ciscoInterface.append((PrepareCiscoInterfaceVe(k,InteVeModel[k])))
					
	return ciscoInterface

###############################################################################

def FindStats(InteVeModel):

	i = 0
	nonvalid_counter = 0
	nonvalid_Ve = []
	vrrp_full_Ve = []
	non_vrrp_Ve = []
	vrrp_mixte_Ve = []
	
	for k,v in InteVeModel.iteritems():
		if InteVeModel[k]['ve_type_v4'] == 'NON-VALIDE':
			nonvalid_Ve.append(k)

		if InteVeModel[k]['ve_type_v4'] == 'V4_VRRP':
			vrrp_full_Ve.append(k)	

		if InteVeModel[k]['ve_type_v4'] == 'V4_NON-VRRP':
			non_vrrp_Ve.append(k)	

		if InteVeModel[k]['ve_type_v4'] == 'V4_MIXTE':
			vrrp_mixte_Ve.append(k)		
	
					
	return nonvalid_Ve,vrrp_full_Ve,non_vrrp_Ve,vrrp_mixte_Ve

#####################################################################################		

def GenerateBrocadeConfig(ve_type,InteVeModel):


	i = 0
	brocadeInterface = []

	
	for k,v in InteVeModel.iteritems():
		#if InteVeModel[k]['ve_type_v4'] != 'NON-VALIDE':
		if ve_type == 'NON-VALIDE':
			brocadeInterface.append('no interface ve ' + k)
			brocadeInterface.append('\n')

		elif InteVeModel[k]['ve_type_v4'] == ve_type:	
			brocadeInterface.append('interface ve ' + k)
			brocadeInterface.append('\n')
			brocadeInterface.append('disable')
			brocadeInterface.append('\n')
			brocadeInterface.append('end')
			brocadeInterface.append('\n')
		
					
	return brocadeInterface

###############################################################################

#def FtnInterfaceVe_VRRP_FINDER (source,vlan,index,indexBegin,indexEnd,nbreV4vrid,nbreV6vrid,nbreIpAddress,nbreV6IpAddress,vrf,accessListIn,accessListOut,ip_mtu,ve_dict):
def FtnInterfaceVe_VRRP_FINDER (source,vlan,index,indexBegin,indexEnd,nbreV4vrid,nbreV6vrid,nbreIpAddress,nbreV6IpAddress,vrf,accessListIn,accessListOut,ip_mtu,interface_ve_dict):
	
	#global interface_ve_dict


	localIndexBegin = indexBegin - 1
	localIndexEnd = indexEnd 
	lcl_ip_mtu = ip_mtu.strip('\n')
	vrf_Name = vrf.strip('\n')
	access_list_IN = accessListIn.strip('\n').strip ('ip access-group').strip('in')
	access_list_OUT = accessListOut.strip('\n').strip ('ip access-group').strip('out')
	vlantest = vlan.strip('\n')

	lcl_string = ''
	
	strtest = ''
	
	StringExtractIndex = []
	
	counter_ipv4 = 0
	counter_ipv6 = 0
	counter_iphelper = 0
	counter_iphelperv6 = 0
	counter_vip_v6 = 0
	
	strtest1 = ''
	
	ipv4_address = []
	ipv6_address = []
	ipv4_helper_address = []
	ipv6_helper_address = []
	interface_vlan_type = ''

	
	
	if(localIndexBegin == localIndexEnd):
		# catching not defined interface ve. Only name Interface ve in config
		StringExtractIndex = source[localIndexBegin]
	else:
		StringExtractIndex = source[localIndexBegin:localIndexEnd]

	
	
	

	# Search number of subnet configured
	lcl_string = ''.join(StringExtractIndex)

	print(':: %s' % '')
	print('vlan: %s' % vlantest)

	'''
	#For Test and debug purpose
	if(vlan == '1142'):
		print StringExtractIndex
		exit()
	'''	
	#print ip_mtu
	


	for m in re.finditer('ip address \d+\.\d+\.\d+\.\d+/\d\d', lcl_string):
		counter_ipv4 = counter_ipv4 + 1
		#print('ip address found:', m.start(), m.end())
		strtest1 = lcl_string[(m.start()+11):(m.end())]
		(interface_ve_dict[vlantest]['ipv4']).append(strtest1)
		ipv4_address.append(strtest1)

	for m in re.finditer('ip-address \d+\.\d+\.\d+\.\d+', lcl_string):
		#print('ip address found:', m.start(), m.end())
		strtest1 = lcl_string[(m.start()+10):(m.end())]
		(interface_ve_dict[vlantest]['vip-v4']).append(strtest1)
			
	for m in re.finditer('ip helper-address \d+\.\d+\.\d+\.\d+', lcl_string):
		counter_iphelper = counter_iphelper + 1
		strtest1 = lcl_string[(m.start()+18):(m.end())]
		#print('ip address found:', m.start(), m.end())	
		(interface_ve_dict[vlantest]['ip-helper']).append(strtest1)

	for m in re.finditer('ipv6 address .+/.+', lcl_string):
		counter_ipv6 = counter_ipv6 + 1
		strtest1 = lcl_string[(m.start()+12):(m.end())]
		(interface_ve_dict[vlantest]['ipv6']).append(strtest1)
		#print('ip address found:', m.start(), m.end())
		ipv6_address.append(strtest1)	
		

	for m in re.finditer('ipv6-address .+', lcl_string):
		counter_vip_v6 = counter_vip_v6 + 1
		strtest1 = lcl_string[(m.start()+12):(m.end())]
		print('ip address found:', m.start(), m.end())	
		(interface_ve_dict[vlantest]['vip-v6']).append(strtest1)
		
	'''
	#For Test and debug purpose
	if(vlan == '503'):
		print counter_ipv6
		print counter_vip_v6
		exit()
	
	'''
	

	if nbreIpAddress  == 0:
		#non_valide_int_ve.append(StringExtractIndex[0].strip('\n').strip('interface ve'))
		interface_vlan_type = 'NON-VALIDE'
		(interface_ve_dict[vlantest]['ve_type_v4']) = interface_vlan_type
		interface_vlan_type = 'Non Valide'
		print ('interface-vlan-type: %s' % interface_vlan_type)

	elif nbreV4vrid == nbreIpAddress:
		interface_ve_dict[vlantest]['ve_type_v4'] = 'V4_VRRP'
		#interface_vlan_type = 'V4_VRRP'
		#print ('interface-vlan-type: %s' % interface_vlan_type)


	elif ((nbreV4vrid == 0) and (nbreIpAddress >= 1)):
		
		#non_vrrp_int_ve.append(StringExtractIndex[0].strip('\n').strip('interface ve'))
		(interface_ve_dict[vlantest]['ve_type_v4']) = 'V4_NON-VRRP'
		interface_vlan_type = 'V4_NON-VRRP'
		print ('interface-vlan-type: %s' % interface_vlan_type)

	elif  nbreIpAddress > nbreV4vrid:
		#mixte_vrrp_int_ve.append(StringExtractIndex[0].strip('\n').strip('interface ve'))
		(interface_ve_dict[vlantest]['ve_type_v4']) = 'V4_MIXTE'
		interface_vlan_type = 'V4_MIXTE'
		print ('interface-vlan-type: %s' % interface_vlan_type)	

	
	if nbreV6IpAddress != 0:
		if ((nbreV6vrid == nbreV6IpAddress)):
			(interface_ve_dict[vlantest]['ve_type_v6']) = 'V6_VRRP'
			interface_vlan_type = 'V6_VRRP'
			print ('interface-vlan-type: %s' % interface_vlan_type)	

		elif ((nbreV6IpAddress == 0) and (nbreV6IpAddress >=1)):
			(interface_ve_dict[vlantest]['ve_type_v6']) = 'V6_NON_VRRP'
			interface_vlan_type = 'V6_NON_VRRP'
			print ('interface-vlan-type: %s' % interface_vlan_type)	
		
		elif ((nbreV6IpAddress> nbreV6vrid)):
			(interface_ve_dict[vlantest]['ve_type_v6']) = 'V6_MIXTE'
			interface_vlan_type = 'MIXTE_V6'
			print ('interface-vlan-type: %s' % interface_vlan_type)		


	'''
	#For Test and debug purpose
	if(vlan == '4035'):
		print interface_ve_dict[vlantest]
		print counter_ipv6
		print counter_vip_v6
		print nbreV6IpAddress 
		exit()
	'''


	lcl_string = ''
	print('nbre ipv4_Vrid: %s' % nbreV4vrid)
	print('nbre ipv4 address: %s' % counter_ipv4)
	print('nbre ipv6 address: %s' % counter_ipv6)
	print('nbre ipv6_Vrid: %s' % nbreV6vrid)
	print('nbre ipv4 ip-helper: %s' % counter_iphelper)
	print ('access-list-in: %s' % access_list_IN)
	print ('access-list-out: %s' % access_list_OUT)
	print ('vrf: %s' % vrf_Name	)
	print ('ip-mtu: %s' % lcl_ip_mtu)
	print "ipv4-list: %s" %  ipv4_address 
	print ('ipv6-list: %s' % ipv6_address)
	print ('ipv4-helper-list: %s' % ipv4_helper_address)
	print('ipv4-end-INNER: %s' % interface_ve_dict[vlantest])	
		
	return 

	#####################################	



