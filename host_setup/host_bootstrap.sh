#!/bin/bash

set -e
install_user=dvossel
home_dir=/home/$install_user
go_dir=$home_dir/go

setenforce 0
sed -i "s/^SELINUX=.*/SELINUX=permissive/" /etc/selinux/config

echo "SETTING SUDOERS"
echo "$install_user ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers
echo "Cmnd_Alias VAGRANT_EXPORTS_ADD = /usr/bin/tee -a /etc/exports" >> /etc/sudoers
echo "Cmnd_Alias VAGRANT_NFSD_CHECK = /usr/bin/systemctl status --no-pager nfs-server.service" >> /etc/sudoers
echo "Cmnd_Alias VAGRANT_NFSD_START = /usr/bin/systemctl start nfs-server.service" >> /etc/sudoers
echo "Cmnd_Alias VAGRANT_NFSD_APPLY = /usr/sbin/exportfs -ar" >> /etc/sudoers
echo "Cmnd_Alias VAGRANT_EXPORTS_REMOVE = /bin/sed -r -e * d -ibak /*/exports" >> /etc/sudoers
echo "Cmnd_Alias VAGRANT_EXPORTS_REMOVE_2 = /bin/cp /*/exports /etc/exports" >> /etc/sudoers
echo "%vagrant ALL=(root) NOPASSWD: VAGRANT_EXPORTS_ADD, VAGRANT_NFSD_CHECK, VAGRANT_NFSD_START, VAGRANT_NFSD_APPLY, VAGRANT_EXPORTS_REMOVE, VAGRANT_EXPORTS_REMOVE_2" >> /etc/sudoers


echo "INSTALLING RPMS"
dnf update -y
dnf install -y sudo docker rsync vim vagrant vagrant-cachier libvirt make qemu-system-x86 libguestfs-tools-c expect nfs-utils golang libvirt-devel vim-go ctags xz

systemctl enable nfs-server
systemctl disable firewalld
systemctl stop firewalld
systemctl restart virtlogd
systemctl restart libvirtd


echo "SETTING GOPATH"
echo "export GOPATH=$go_dir" >> $home_dir/.bashrc
echo "export PATH=\$PATH:$go_dir/bin" >> $home_dir/.bashrc

source $home_dir/.bashrc

mkdir -p $go_dir
cd $GOPATH
echo "GOPATH SET TO $PWD"

echo "INSTALLING GO DEPS"
# Use goimports for package import ordering
go get golang.org/x/tools/cmd/goimports
go get -u github.com/golang/dep/cmd/dep
go get -u github.com/golang/mock/gomock
go get -u github.com/rmohr/mock/mockgen
go get -u github.com/rmohr/go-swagger-utils/swagger-doc

chown -R $install_user: $GOPATH

gpasswd -a ${install_user} libvirt
newgrp libvirt
gpasswd -a $install_user vagrant

cd $home_dir

echo "export VAGRANT_CACHE_RPM=true" >> .bashrc
echo "export VAGRANT_CACHE_DOCKER=true" >> .bashrc
echo "alias kubectl=\"cluster/kubectl.sh\"" >> .bashrc
echo "alias virtctl=\"bin/virtctl\"" >> .bashrc

#dnf install kernel-devel kernel-headers gcc dkms acpid
#http://us.download.nvidia.com/XFree86/Linux-x86_64/381.22/NVIDIA-Linux-x86_64-381.22.run

# nested virtualization
sudo rmmod kvm-intel
sudo sh -c "echo 'options kvm-intel nested=y' >> /etc/modprobe.d/dist.conf"
sudo modprobe kvm-intel

sudo groupadd docker
sudo usermod -aG docker dvossel
