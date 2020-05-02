# Phase 3

**BCrypt Porject Link** - [BCrypt](https://github.com/pyca/bcrypt)

## Code used by Author Shazmaan

**Code can be found in views.py** - [views.py](https://github.com/Shazmaan)

<update this link when merged>

### Creating Hash + Salt Password

```
In views.py line:

hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())

Source code line:

def hashpw(password, salt):
    if isinstance(password, six.text_type) or isinstance(salt, six.text_type):
        raise TypeError("Unicode-objects must be encoded before hashing")
....

```
* Why did I use this code?

The library bcrypt handles hash + salt encryption and writing a SHA-256 algorithm on it's own is difficult.

* How does the code do what it does?

First, bcrypt.gensalt() calls

```
def gensalt(rounds=12, prefix=b"2b"):
    if prefix not in (b"2a", b"2b"):
        raise ValueError("Supported prefixes are b'2a' or b'2b'")
....
```
which generates a random salt for hashing password.

```
retval = _bcrypt.lib.bcrypt_hashpass(password, salt, hashed, len(hashed))

```
which hashes + salts the given password to convert to encrypted password.

* Licensing?

Apache Software License (Apache License, Version 2.0)

### Checking password

```
In code:

if bcrypt.checkpw(password, stored_password):
....

In source code:

def checkpw(password, hashed_password):
    if (isinstance(password, six.text_type) or
....

```
* Why did I use this code?

The library compares the given byte encoded password with the hashed_password with multiple salts which is easier then creating such functions
on our own.

* How does the code do what it does?

The source code here calls hashpw which in return generates a hashed_password and this password is then checked with the given hashed_password.
As the salt generated is random, the password is checked with multiple salts.

* Licensing?

Apache Software License (Apache License, Version 2.0)