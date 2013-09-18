#!/usr/bin/env python
import os
import sys

def main(argv):
	rpm_path = argv[1]
	for arg in argv:
		if argv[0] == arg or argv[1] == arg:
			continue

		cluster_rpms(arg, rpm_path)

def cluster_rpms(host, path):

	os.system("ssh -l root %s yum remove -y pacemaker pacemaker-cli pacemaker-cluster-libs pacemaker-cts pacemaker-debuginfo pacemaker-doc pacemaker-libs pacemaker-libs-devel pacemaker-remote" % host)
	os.system("ssh -l root %s yum remove -y /root/cluster_rpms/*.rpm" % host)

	os.system("ssh -l root %s rm -rf /root/cluster_rpms" % host)
	os.system("ssh -l root %s mkdir /root/cluster_rpms" % host)

	os.system("scp -r %s/* root@%s:/root/cluster_rpms" % (path, host))
	os.system("ssh -l root %s rpm -Uvh /root/cluster_rpms/*.rpm" % host)

if __name__=="__main__":
	main(sys.argv)
