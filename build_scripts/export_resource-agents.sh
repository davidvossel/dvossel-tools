#!/bin/sh

TAG=$(git log --pretty="format:%h" -n 1)
distdir="ClusterLabs-resource-agents-${TAG}"
TARFILE="${distdir}.tar.gz"

rm -rf $TARFILE $distdir

git archive --prefix=$distdir/ HEAD | gzip > $TARFILE
