#!/bin/bash
#. /usr/share/cluster/utils/fs-lib.sh

iterations=100
fake_mounts=5
tmpfile="/tmp/fs_test/fs-file"
device="/dev/loop1"
agent="/usr/share/cluster/fs.sh"

setup()
{
	mkdir -p /tmp/fs_test/mount
	fallocate -l 50M $tmpfile
	losetup $device $tmpfile
	mke2fs -t ext4 -F $device > /dev/null 2>&1

	mkdir -p /tmp/fs_test/fake
	mkdir -p /tmp/fs_test/fake2

	for i in $(seq $fake_mounts)
	do
		mount --bind /tmp/fs_test/fake /tmp/fs_test/fake2
	done

}

cleanup()
{
	for i in $(seq $fake_mounts)
	do
		umount /tmp/fs_test/fake2
	done
	losetup -d $device
	rm -rf /tmp/fs_test
}

check_not_running()
{

	output=$($agent monitor 2>&1)

	if [ $? -ne 7 ]; then
		echo "Monitor failed... shouldn't be running. rc=$res iteration=$2"
		echo "$output"
	fi
}

exec()
{
	output=$($agent $1 2>&1)
	if [ $? -ne 0 ]; then
		echo "$1 failed. rc=$res iteration=$2"
		echo "$output"
	fi
}

test1()
{
	export OCF_RESKEY_name="performance_test"
	export OCF_RESKEY_mountpoint=/tmp/fs_test/mount
	export OCF_RESKEY_device=$device
	export OCF_RESKEY_fstype=ext4

	echo "Timing $iterations iterations of fs.sh start/stop"
	start=$(date +"%s")
	for i in $(seq $iterations)
	do
		exec "start" "$i"
		exec "monitor" "$i"
		exec "stop" "$i"
		check_not_running
	done
	end=$(date +"%s")
	time=$(($end - $start))
	echo "Test done.  ${time}s"
}

test2()
{
	agent="/usr/share/cluster/netfs.sh"
	export OCF_RESKEY_name="performance_test"
	export OCF_RESKEY_mountpoint=/tmp/fs_test/mount
	export OCF_RESKEY_host="192.168.122.80"
	export OCF_RESKEY_export="/"
	export OCF_RESKEY_fstype=nfs4

	echo "Timing $iterations iterations of fs.sh start/stop"
	start=$(date +"%s")
	for i in $(seq $iterations)
	do
		exec "start" "$i"
		exec "monitor" "$i"
		exec "stop" "$i"
		check_not_running
	done
	end=$(date +"%s")
	time=$(($end - $start))
	echo "Test done.  ${time}s"

}

cleanup
setup
test1
#test2
cleanup
