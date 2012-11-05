#!/usr/bin/env python
import os
import sys

def main(argv):

	for arg in argv:
		if argv[0] == arg:
			continue

		run_kill(arg)

def run_kill(host):
	os.system("ssh -l \"root\" %s killall -q -9 corosync aisexec heartbeat pacemakerd ccm stonithd ha_logd lrmd crmd pengine attrd pingd mgmtd cib fenced dlm_controld gfs_controld" % host)
	os.system("ssh -l \"root\" %s \"service corosync stop\"" % host)
	os.system("ssh -l \"root\" %s \"service pacemaker stop\"" % host)

if __name__=="__main__":
	main(sys.argv)

