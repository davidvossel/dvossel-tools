#!/usr/bin/env python
import os
import sys

def main(argv):

	for arg in argv:
		if argv[0] == arg:
			continue
		
		run_clean(arg)

def run_clean(host):
	os.system("ssh -l \"root\" %s killall -q -9 corosync aisexec heartbeat pacemakerd ccm stonithd ha_logd lrmd crmd pengine attrd pingd mgmtd cib fenced dlm_controld gfs_controld" % host)

	os.system("ssh -l \"root\" %s \"rm -rf /var/lib/heartbeat/crm/cib*\"" % host)
	os.system("ssh -l \"root\" %s \"service corosync stop\"" % host)
	os.system("ssh -l \"root\" %s \"service pacemaker stop\"" % host)

	os.system("ssh -l \"root\" %s \"rm -rf /var/lib/heartbeat/crm/cib-* /var/lib/pacemaker/cib/* /var/lib/pacemaker/blackbox/* /var/lib/pacemaker/pengine/* /var/lib/heartbeat/cores/*/core.* /var/lib/heartbeat/hostcache /var/lib/openais/core.* /var/lib/corosync/core.* var/lib/oprofile/samples/cts.*\"" % host)
	os.system("ssh -l \"root\" %s \"find /var/lib/pengine -name '*.bz2' -exec rm -f \{\} \;\"" % host)

#	os.system("ssh -l root %s yum install -y httpd fence-virt fence-virtd-multicast qarsh-server xinetd fence-virtd-libvirt nmap" % host)

	os.system("ssh -l root %s yum remove -y pacemaker pacemaker-cli pacemaker-cluster-libs pacemaker-cts pacemaker-debuginfo pacemaker-doc pacemaker-libs pacemaker-libs-devel" % host)

	os.system("scp -r /home/dvossel/rpmbuild/RPMS/x86_64 root@%s:/root" % (host))
	os.system("ssh -l root %s yum install -y /root/x86_64/*.rpm" % host)

	os.system("ssh -l \"root\" %s mkdir /etc/cluster" % host)
	os.system("scp /etc/cluster/fence_xvm.key %s:/etc/cluster/fence_xvm.key" % host)

	os.system("ssh -l \"root\" %s chkconfig libvirtd off" % host)

	os.system("ssh -l \"root\" %s chown :root /var/log/cluster" % host)
	os.system("ssh -l \"root\" %s chmod 776 /var/log/cluster/" % host)

	os.system("ssh -l \"root\" %s chkconfig xinetd on" % host)
	os.system("ssh -l \"root\" %s service xinetd start &> /dev/null" % host)

if __name__=="__main__":
	main(sys.argv)

