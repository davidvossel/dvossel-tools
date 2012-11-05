#!/usr/bin/env python
import os
import sys

def main(argv):
	nodes = 1;

	if len(argv) > 3:
		nodes = len(argv) - 2;

	cfg = ("""compatibility: whitetank
totem {
        version: 2
        token:          5000
        token_retransmits_before_loss_const: 10
        join:           1000
        consensus:      6000
        vsftype:        none
        max_messages:   20
        send_join: 45
        clear_node_high_bit: yes
        secauth:        off
        threads:           0
        interface {
                ringnumber: 0

                # The following values need to be set based on your environment
                bindnetaddr: 192.168.122.0
                mcastaddr: 226.94.1.1
                mcastport: 4000
        }
}
logging {
        debug: off
        fileline: off
        to_syslog: yes
        to_stderr: off
        to_logfile:yes
		logfile: /var/log/cluster.log
        syslog_facility: daemon
        timestamp: on
}
amf {
        mode: disabled
}
quorum {
   provider: corosync_votequorum
   expected_votes: %d
   votes: 1
   wait_for_all: 0
   last_man_standing: 0
   auto_tie_breaker: 0
}""" % (nodes))


	f = open('corosync.conf', 'w+')
	f.write(cfg)
	f.close()

if __name__=="__main__":
	main(sys.argv)
