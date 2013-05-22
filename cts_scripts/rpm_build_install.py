#!/usr/bin/env python
import os
import sys
import subprocess
import shlex

class TestOptions:
	def __init__(self):
		self.options = {}
		self.options['show-usage'] = 0
		self.options['src-dir'] = "/home/dvossel/pacemaker_vossel"
		self.options['build'] = 1
		self.options['rhel_build'] = 0
		self.options['host_install'] = 0
		self.options['nodes'] = ""

	def build_options(self, argv):
		args = argv[1:]
		skip = 0
		for i in range(0, len(args)):
			if skip:
				skip = 0
				continue
			elif args[i] == "-h" or args[i] == "--help":
				self.show_usage()
				sys.exit(0)
			elif args[i] == "-b":
				self.options['build'] = 1
			elif args[i] == "-r":
				self.options['rhel_build'] = 1
			elif args[i] == "-i":
				self.options['host_install'] = 1
			elif args[i] == "-s":
				self.options['src-dir'] = args[i+1]
				skip = 1
			elif args[i] == "-n":
				self.options['nodes'] = args[i+1]
				print "installing on nodes %s" % self.options['nodes']
				skip = 1

	def show_usage(self):
		print "usage: " + sys.argv[0] + " [options]"
		print "Options:"
		print "\t [-n]                       nodes"
		print "\t [-s]                       src dir"
		print "\t [-b]                       fedora build and distribute rpms (DEFAULT)"
		print "\t [-r]                       rhel build and distribute rpms"
		print "\t [-i]                       install rpms on host"

def output_from_command(command, no_wait=0):
	test = subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE)

	if no_wait == 0:
		test.wait()
	else:
		return 0

	return test.communicate()[0].split("\n")

def main(argv):
	o = TestOptions()
	o.build_options(argv)

	curdir = os.getcwd();
	prefix = "%s/helper_scripts" % curdir

	#build rpms
	if o.options['build']:
		builder = subprocess.Popen(shlex.split("helper_scripts/fedora_make_rpms %s" % o.options['src-dir']))
		builder.wait()

	if o.options['rhel_build']:
		builder = subprocess.Popen(shlex.split("helper_scripts/rhel_make_rpms %s" % o.options['src-dir']))
		builder.wait()

	if o.options['host_install']:
		our_uname = output_from_command("uname -n")
		if our_uname:
			our_uname = our_uname[0]
		os.system("python %s/install_cluster_rpms.py %s/pacemaker_rpms %s" % (prefix, curdir, our_uname))

	#clean nodes and send rpms out
	if o.options['nodes'] != "" :
		nodes = o.options['nodes'].split(' ')
		for node in nodes:
			install_rpms(node, o)

def install_rpms(host, o):
	curdir = os.getcwd();
	prefix = "%s/helper_scripts" % curdir
	os.system("python %s/kill_cluster.py %s" % (prefix, host))
	os.system("python %s/install_cluster_rpms.py %s/pacemaker_rpms %s" % (prefix, curdir, host))

if __name__=="__main__":
	main(sys.argv)

