# QTIP Developer Guide

This guide is about how to **develop** QTIP.

If you just want to use it for performance benchmark, check the user guide
instead.

## Getting Started

### Source code

```bash
~$ git clone https://gerrit.opnfv.org/gerrit/qtip
```

### VirtualEnv

It is recommended to use [virtualenv](https://virtualenv.pypa.io) to isolate
your development environment from system, especially when you are working on
several different projects.

### Testing

QTIP use [tox](https://tox.readthedocs.io) to automate the testing tasks

```bash
$ pip install tox
$ tox
```

Undering macOS system, it will happen to a **fatal error** when installing package `cryptograph`:

```
'openssl/opensslv.h' file not found
#incude <openssl/opensslv.h>
    ^
1 error generated.
```

It is for macOS uses TLS instead of OpenSSL and no header files supported. The solutions is:
``` code=bash
# brew install openssl

# #add these lines in to your shell profiles, such as .bash_profile, .zshrc
# export CPPFLAGS='-I $openssl_install_path/include'
# export LDFLAGS='-L $openssl_install_path/lib'
```

## Architecture

**TODO**: move to design spec

QTIP has a flexible architecture to allow different deployment mode

- **Standalone**: full feature performance benchmark platform.
- **Agent**: minimal agent driven by external test runners.

### Standalone Mode (Solo)

QTIP instance deployed in container, VM or host generate benchmark report and
push data to Indices Hub for storage and visualization.

![solo](https://wiki.opnfv.org/download/attachments/8687017/Standalone.png?api=v2)

### Agent Mode (Melody)

QTIP Collector and Reporter driven by external test framework or runner such as
[yardstick](https://wiki.opnfv.org/display/yardstick),
[pytest](http://doc.pytest.org/) and etc.

![melody](https://wiki.opnfv.org/download/attachments/8687017/Agent.png?api=v2)

## Core Modules

TBD

- loader
- runner
- collector
- reporter

## Drivers

TBD

- ansible
- yardstick

## Interfaces

### Agent

TBD

### CLI

Click currently supports Bash completion. The prerequisite for this is that the program
needs to be installed correctly. To install Qtip, execute the following command in root
folder of Qtip:

```

cd <project root>
pip install -e .

```

Once the installation has been completed successfully, the following needs to be added to
the `.bashrc` file:

```
eval "$(_QTIP_COMPLETE=source qtip)"
```

The above would activate command completion for Qtip.

### API

TBD

## Assets

**TODO**: move to user guide

- benchmark plan
- QPI spec
- metric spec

## Docker Image

TBD

## Annex

### Directories

TBD
