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
		self.options['build'] = "true"
		self.options['nodes'] = ""
		self.options['stack'] = "coro"
		self.options['launch_script'] = ""
		self.options['launch_parameters'] = ""

	def build_options(self, argv):
		args = argv[1:]
		skip = 0
		for i in range(0, len(args)):
			if skip:
				skip = 0
				continue
			elif args[i] == "-h" or args[i] == "--help":
				self.options['show-usage'] = 1
			elif args[i] == "-b":
				self.options['build'] = args[i+1]
				skip = 1
			elif args[i] == "-s":
				self.options['src-dir'] = args[i+1]
				skip = 1
			elif args[i] == "-n":
				self.options['nodes'] = args[i+1]
				print "installing on nodes %s" % self.options['nodes']
				skip = 1
			elif args[i] == "-c":
				self.options['stack'] = args[i+1]
				skip = 1
			elif args[i] == "-l":
				self.options['launch_script'] = args[i+1]
				skip = 1
			elif args[i] == "-p":
				self.options['launch_parameters'] = args[i+1]
				skip = 1

	def show_usage(self):
		print "usage: " + sys.argv[0] + " [options]"
		print "Options:"
		print "\t [-n]                       nodes"
		print "\t [-s]                       src dir"
		print "\t [-b]                       build"
		print "\t [-c]                       stack"
		print "\t [-p]                       launch parameters"
		print "\t [-l]                       launch script" ## finish this

def main(argv):
	o = TestOptions()
	o.build_options(argv)

	#build rpms
	if o.options['build'] == "true":
		builder = subprocess.Popen(shlex.split("helper_scripts/make_rpms %s" % o.options['src-dir']))
		builder.wait()

	#clean nodes and send rpms out
	if o.options['nodes'] != "" :
		nodes = o.options['nodes'].split(' ')
		for node in nodes:
			run_clean(node, o)

	# launch cts if we have a script and parameters
	if o.options['launch_script'] and o.options['launch_parameters']:
		cmd = ("launch_scripts/%s %s" % (o.options['launch_script'], o.options['launch_parameters']))
		cts = subprocess.Popen(shlex.split(cmd))
		cts.wait()

def run_clean(host, o):

	curdir = os.getcwd();
	prefix = "%s/helper_scripts" % curdir

	os.system("python %s/kill_cluster.py %s" % (prefix, host))
	os.system("python %s/clear_cluster_cache.py %s" % (prefix, host))
	os.system("python %s/install_cluster_rpms.py %s/pacemaker_rpms %s" % (prefix, curdir, host))

	if o.options['stack'] == "coro":
		os.system("python %s/corosync2_cfg_gen.py %s" % (prefix, o.options['nodes']))
		os.system("scp corosync.conf %s:/etc/corosync/corosync.conf" % (host))

	os.system("scp pacemaker.sysconfig %s:/etc/sysconfig/pacemaker" % (host))

	os.system("python %s/mis_setup.py %s" % (prefix, host))

if __name__=="__main__":
	main(sys.argv)

