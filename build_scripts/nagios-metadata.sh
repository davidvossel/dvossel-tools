#!/bin/sh

TAG=$(git log --pretty="format:%h" -n 1)
distdir="nagios-agents-metadata-${TAG}"
TARFILE="${distdir}.tar.gz"

rm -rf $TARFILE $distdir

git archive --prefix=$distdir/ HEAD | gzip > $TARFILE
