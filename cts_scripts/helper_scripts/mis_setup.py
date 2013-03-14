#!/usr/bin/env python
import os
import sys

def main(argv):
	for arg in argv:
		if argv[0] == arg:
			continue

		mis_cluster_setup(arg)

#place for random setup environment stuff nodes need for cts
def mis_cluster_setup(host):
	os.system("ssh -l root %s yum install -y fence-virt fence-virtd-multicast qarsh-server xinetd fence-virtd-libvirt nmap" % host)
	os.system("ssh -l \"root\" %s mkdir /etc/cluster" % host)
	os.system("scp /etc/cluster/fence_xvm.key %s:/etc/cluster/fence_xvm.key" % host)

###	os.system("ssh -l \"root\" %s chkconfig libvirtd off" % host)

	os.system("ssh -l \"root\" %s chown :root /var/log/cluster" % host)
	os.system("ssh -l \"root\" %s chmod 776 /var/log/cluster/" % host)

	os.system("ssh -l \"root\" %s chkconfig xinetd on" % host)
	os.system("ssh -l \"root\" %s service xinetd start &> /dev/null" % host)

if __name__=="__main__":
	main(sys.argv)
