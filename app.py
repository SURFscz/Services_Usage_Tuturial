#!/usr/bin/env python3

import os
import sys
import ldap

# My log function...
def log_debug(s):
	print(s)

# Panic function...
def panic(s):
	log_debug(s)
	sys.exit(1)

# Get environment constants...

LDAP_HOST = os.environ.get("LDAP_HOST", "localhost")
LDAP_BASE = os.environ.get("LDAP_BASE", "")
LDAP_BIND = os.environ.get("LDAP_BIND", "admin")
LDAP_PASS = os.environ.get("LDAP_PASS", "changeme")

# This part is connnection to the LDAP...
ldap_session = None

try:
	ldap_session = ldap.initialize(f"ldaps://{LDAP_HOST}")
	ldap_session.bind_s(LDAP_BIND, LDAP_PASS)
except Exception as e:
	if ldap_session:
		ldap_session.unbind_s()
	panic(f"LDAP connection failed ! {str(e)}")

def log_ldap_result(r):
	log_debug(f"[LDAP SEARCH RESULT]")

	if not r:
		log_debug("<empty>")
	elif len(r) == 0:
		log_debug("[]")
	else:
		for i in r:
			log_debug(f"\tDN:\t{i[0]}\n\tDATA:\t{i[1]}")


# Lookup service...
def ldap_services(base):
	l = ldap_session.search_s(base, ldap.SCOPE_SUBTREE, f"(&(objectclass=organization)(dc=*))")
#	log_ldap_result(l)
	return l

# Lookup collaborations linked to my service...
def ldap_collaborations(base):
	l = ldap_session.search_s(base, ldap.SCOPE_ONELEVEL, f"(&(objectclass=organization)(o=*))")
#	log_ldap_result(l)
	return l

# Find all people within a certain subtree...
def ldap_people(base):
	l = ldap_session.search_s(f"ou=People,{base}", ldap.SCOPE_ONELEVEL, f"(&(objectclass=person)(uid=*))")
#	log_ldap_result(l)
	return l

# Find all groups within a certain subtree...
def ldap_groups(base):
	l = ldap_session.search_s(f"ou=Groups,{base}", ldap.SCOPE_ONELEVEL, f"(&(objectclass=sczGroup)(cn=*))")
#	log_ldap_result(l)
	return l

# Find groups where person 'ismemberof'...
def ldap_groups_of_person(base, person):
	l = ldap_session.search_s(f"ou=Groups,{base}", ldap.SCOPE_ONELEVEL, f"(&(objectclass=sczGroup)(sczMember={person}))")
#	log_ldap_result(l)
	return l

# Traverse all CO's connected to my service

for s in ldap_services(LDAP_BASE):
	log_debug(f"* Service: {s[1]['dc'][0].decode()}")

for co in ldap_collaborations(LDAP_BASE):
	log_debug(f"** Collaboration: {co[1]['description'][0].decode()}")

	# For each CO, traverse all people that are member of this CO
	for p in ldap_people(co[0]):
		log_debug(f"*** Person: {p[1]['uid'][0].decode()}")

		ldap_groups_of_person(co[0], p[0])

	# For each CO, traverse all groups, report all members of that Group...
	for g in ldap_groups(co[0]):
		log_debug(f"*** Group: {g[1]['cn'][0].decode()}")

		for u in g[1]['sczMember']:
			log_debug(f"**** Member: {u.decode().split(',')[0].split('=')[1]}")
