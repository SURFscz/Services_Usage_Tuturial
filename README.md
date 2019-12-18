# Howto

Author: Harry Kodden <harry.kodden@surfnet.nl>

This sample shows how to make use of the Service LDAP offered by Science Collaboration Zone (SCZ)

## Configuration

Prepare a file **.env** which contains following constants:

```
LDAP_HOST=...hostname of ldap...
LDAP_PASS=...bind password...
LDAP_BIND=...bind dn...
LDAP_BASE=...base dn...
```

### Run the sample

You can either use **docker-compose** or just run the **start.sh** script.

usage with **docker-compose**:

```
docker-compose build
docker-compose up
```

usage with **start.sh**

```
$ start.sh
```
