#!/usr/bin/env python
import os
import sys

def main(argv):

	for arg in argv:
		if argv[0] == arg:
			continue

		clear_cache(arg)

def clear_cache(host):
	os.system("ssh -l \"root\" %s \"rm -rf /var/log/cts.log\"" % host)
	os.system("ssh -l \"root\" %s \"rm -rf /var/log/pacemaker.log\"" % host)
	os.system("ssh -l \"root\" %s \"rm -rf /var/lib/heartbeat/crm/cib*\"" % host)
	os.system("ssh -l \"root\" %s \"rm -rf /var/lib/heartbeat/crm/cib-* /var/lib/pacemaker/cib/* /var/lib/pacemaker/cores/* /var/lib/pacemaker/blackbox/* /var/lib/pacemaker/pengine/* /var/lib/heartbeat/cores/*/core.* /var/lib/heartbeat/hostcache /var/lib/openais/core.* /var/lib/corosync/core.* var/lib/oprofile/samples/cts.*\"" % host)
	os.system("ssh -l \"root\" %s \"find /var/lib/pengine -name '*.bz2' -exec rm -f \{\} \;\"" % host)

if __name__=="__main__":
	main(sys.argv)
