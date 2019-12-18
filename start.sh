#!/bin/bash

# Make available my configuration...
source .env

# Build my image...
docker build -t sample .

# Run my container !
docker run \
      -e LDAP_HOST=${LDAP_HOST} \
      -e LDAP_BIND=${LDAP_BIND} \
      -e LDAP_PASS=${LDAP_PASS} \
      -e LDAP_BASE=${LDAP_BASE} \
      -ti \
      sample
