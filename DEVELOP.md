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

TBD

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
