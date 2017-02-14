[![Build Status](https://travis-ci.org/esnet/shibboleth_session_auth.svg?branch=master)](https://travis-ci.org/esnet/shibboleth_session_auth) [![Coverage Status](https://coveralls.io/repos/github/esnet/shibboleth_session_auth/badge.svg?branch=master)](https://coveralls.io/github/esnet/shibboleth_session_auth?branch=master)

# shibboleth_session_auth 
## Simplistic Shibboleth integration for Django sessions

This is a very simple way of allowing users to be authenticated via Shibboleth 
but to be a part of Django groups and users. This is accomplished by using
Apache `mod_shib` to protect the provided view. If the user is able to
authenticate then we extract certain details from the data provided by
Shibboleth. The view will create Django Users and Groups as necessary.

### Apache Config

This code has only been tested with `mod_shib` for Apache.

Here's the config we use:

```
<Location /shibboleth-sso/>
  AuthType shibboleth
  ShibCompatWith24 On
  ShibRequestSetting requireSession true
  Require shib-attr member staff
/Location>
```

You may want to tweak or remove the `Require` line depending on your needs.
As it is, it requires users to be a member of group `staff` in order to be
able to authenticate.

### Django Setup

You'll need to add an entry in your `urls.py`, similar to this:

```python
from shibboleth_session_auth.views import shibboleth_session_auth

urlpatterns += [
    url(r'^shibboleth-sso/', shibboleth_session_auth, name="esnet-sso"),
]
```

Note that we use `shibboleth-sso` both here and in the Apache config.

### Django Settings

```python
SHIBBOLETH_SESSION_AUTH = {
    'IDP_ATTRIBUTE': 'Shib-Identity-Provider',
    'AUTHORIZED_IDPS': [
        'https://${YOUR_IDP}/idp/shibboleth',
    ],
    #
    # note that we use Apache environment variables directly rather than the
    # HTTP_xxx variables which are derived from the HTTP request headers.
    # The HTTP_xxx variety is vulnerable to potential spoofing
    #
    'USER_ATTRIBUTES': [
        ('uid', 'username', True),
        ('mail', 'email', True),
        ('givenName', 'first_name', False),
        ('sn', 'last_name', False),
    ],
    'GROUP_ATTRIBUTE': 'member',
    'GROUPS_BY_IDP': {}
}
```

`IDP_ATTRIBUTE` defines which Apache environment variable carries the name of
the IdP.

`AUTHORIZED_IDPS` is a list of IdPs that we trust. The full URL may vary for
your setup -- please check this with whomever runs your IdP..

`USER_ATTRIBUTES` a list of tuples which are used to map from the attribute
names provided by the IdP to fields to be used with the Django User model. The
format is (`idp_attribute`, `django_model_attribute`, `required`).

`GROUP_ATTRIBUTE` is the name used by the IdP to provide group membership.
The user will be added to each group listed in the group attribute. If the
group does not already exist it will be created.  Groups are assumed to be
separated by a semicolon (`;`) in the data provided by the IdP.

`GROUPS_BY_IDP` this is a dictionary mapping an IdP (from `AUTHORIZED_IDPS`)
to a list of groups. If the user is authenticated to the named IdP then
the user will be added to each of the groups, creating the groups as necessary.

