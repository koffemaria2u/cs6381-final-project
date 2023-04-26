#!/usr/bin/env bash

USER=${1:-test}
PW=${2:-test}

htpasswd -b -c demo-users $USER $PW
kubectl -n whoami delete secret whoami-users >& /dev/null
kubectl -n whoami create secret generic whoami-users --from-file=demo-users
rm -rf demo-users >& /dev/null
