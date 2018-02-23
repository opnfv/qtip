##########################################################
# Dockerfile to run a flask-based web application# Based on an ubuntu:16.04
##########################################################

# Set the base image to use to centos
FROM ubuntu:16.04

# Set the file maintainer
MAINTAINER Qiang.Dai@spirent.com
LABEL version="0.1" description="Spirent networking test Docker container"

# Set env varibles used in this Dockerfile (add a unique prefix, such as DOCKYARD)
# Local directory with project source
ENV DOCKYARD_SRC=nettest \
    DOCKYARD_SRCHOME=/opt \
    DOCKYARD_SRCPROJ=/opt/nettest

# Update the defualt application repository source list
RUN apt-get update && apt-get install -y \
    gcc \
    python-dev \
    python-pip \
    python-setuptools \
    --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# Copy application source code to SRCDIR
COPY $DOCKYARD_SRC $DOCKYARD_SRCPROJ

# Create application subdirectories
WORKDIR $DOCKYARD_SRCPROJ
RUN mkdir -p log
VOLUME ["$DOCKYARD_SRCPROJ/log/"]

# Install Python dependencies
RUN pip install -U pip \
    && pip install -U setuptools \
    && pip install -r $DOCKYARD_SRCPROJ/requirements.txt

# Port to expose
EXPOSE 5001

# Copy entrypoint script into the image
WORKDIR $DOCKYARD_SRCPROJ

#CMD ["/bin/bash"]
CMD ["/bin/bash", "start.sh"]
