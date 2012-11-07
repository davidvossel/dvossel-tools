#!/usr/bin/env python
import os
import sys

def main(argv):
	nodes = 1

	if len(argv) > 3:
		nodes = len(argv) - 2;

	cfg = ("""
compatibility: whitetank
totem {
	version: 2
	secauth: off
	threads: 0
	interface {
		ringnumber: 0
		bindnetaddr: 192.168.122.0
		mcastaddr: 226.94.1.1
		mcastport: 4000
		ttl: 1
	}
}
logging {
	fileline: off
	to_stderr: no
	to_logfile: yes
	to_syslog: yes
	logfile: /var/log/cluster/corosync.log
	debug: off
	timestamp: on
	logger_subsys {
		subsys: AMF
		debug: off
	}
}

amf {
	mode: disabled
}""")


	f = open('corosync.conf', 'w+')
	f.write(cfg)
	f.close()

if __name__=="__main__":
	main(sys.argv)
