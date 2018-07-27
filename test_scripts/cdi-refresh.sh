#!/bin/bash

set -e 

regport=32771

docker tag kubevirt/cdi-importer localhost:$regport/kubevirt/cdi-importer
docker tag kubevirt/cdi-controller localhost:$regport/kubevirt/cdi-controller
docker tag kubevirt/cdi-apiserver localhost:$regport/kubevirt/cdi-apiserver
docker tag kubevirt/cdi-uploadproxy localhost:$regport/kubevirt/cdi-uploadproxy

docker push localhost:$regport/kubevirt/cdi-importer
docker push localhost:$regport/kubevirt/cdi-controller
docker push localhost:$regport/kubevirt/cdi-apiserver
docker push localhost:$regport/kubevirt/cdi-uploadproxy

cluster/cli.sh ssh node01 "sudo docker pull registry:5000/kubevirt/cdi-importer"
cluster/cli.sh ssh node01 "sudo docker tag registry:5000/kubevirt/cdi-importer kubevirt/cdi-importer:vossel"
cluster/cli.sh ssh node01 "sudo docker pull registry:5000/kubevirt/cdi-controller"
cluster/cli.sh ssh node01 "sudo docker tag registry:5000/kubevirt/cdi-controller kubevirt/cdi-controller:vossel"
cluster/cli.sh ssh node01 "sudo docker pull registry:5000/kubevirt/cdi-apiserver"
cluster/cli.sh ssh node01 "sudo docker tag registry:5000/kubevirt/cdi-apiserver kubevirt/cdi-apiserver:vossel"
cluster/cli.sh ssh node01 "sudo docker pull registry:5000/kubevirt/cdi-uploadproxy"
cluster/cli.sh ssh node01 "sudo docker tag registry:5000/kubevirt/cdi-uploadproxy kubevirt/cdi-uploadproxy:vossel"

#cluster/kubectl.sh delete -f $GOPATH/src/github.com/kubevirt/containerized-data-importer/manifests/controller/cdi-controller-deployment.yaml
cat $GOPATH/src/kubevirt.io/containerized-data-importer/manifests/controller/cdi-controller-deployment.yaml | sed s/cdi-controller:.*/cdi-controller:vossel/g | sed s/cdi-apiserver:.*/cdi-apiserver:vossel/g |  sed s/cdi-uploadproxy:.*/cdi-uploadproxy:vossel/g> cdi.yaml

set +e
#kubectl apply -f "https://raw.githubusercontent.com/davidvossel/hostpath-pvc-vm-disks-examples/master/storage-setup/install.yaml"
cluster/kubectl.sh delete -f cdi.yaml
set -e
sleep 2
cluster/kubectl.sh create -f cdi.yaml
#cluster/kubectl.sh create -f $GOPATH/src/github.com/kubevirt/containerized-data-importer/manifests/controller/cdi-controller-deployment.yaml

