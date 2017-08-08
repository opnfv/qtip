##########################################
#####Docker container for QTIP############
##########################################

FROM ubuntu:16.04
MAINTAINER Yujun Zhang <zhang.yujunz@zte.com.cn>
LABEL version="0.1" description="OPNFV QTIP Docker container"

ARG BRANCH=master

ENV REPOS_DIR /home/opnfv/repos
ENV PYTHONPATH /home/opnfv/repos/qtip
ENV USER root
WORKDIR /home/opnfv

# Packaged Dependencies
RUN apt-get update && apt-get install -y \
    software-properties-common \
    git \
    gcc \
    build-essential\
    libssl-dev\
    libffi-dev\
    locales \
    supervisor \
    python-dev \
    python-pip \
    python-setuptools \
    rsync \
    iputils-ping \
    --no-install-recommends \
&& rm -rf /var/lib/apt/lists/*

RUN pip install -U pip && pip install -U setuptools

RUN apt-add-repository ppa:ansible/ansible -y
RUN apt-key update -y
RUN apt-get update && apt-get install ansible -y

RUN mkdir -p ${REPOS_DIR}
RUN mkdir -p /root/.ssh
RUN mkdir -p /root/qtip/logs

RUN chmod 700 /root/.ssh

#Cloning Repos
RUN git config --global http.sslVerify false
RUN git clone -b $BRANCH https://gerrit.opnfv.org/gerrit/qtip $REPOS_DIR/qtip

RUN cd $REPOS_DIR/qtip && pip install -U -e .

RUN echo 'eval $(ssh-agent)' >> /root/.bashrc

# Exposing ports
EXPOSE 5000

#Config supervisor
RUN mkdir -p /var/log/supervisor
RUN locale-gen en_US en_US.UTF-8
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

CMD ["/usr/bin/supervisord"]