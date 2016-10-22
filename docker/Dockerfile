##########################################
#####Docker container for QTIP############
##########################################


FROM ubuntu:14.04
MAINTAINER Nauman Ahad <Nauman_Ahad@dell.com>
LABEL version="0.1" description="OPNFV QTIP Docker container"




ENV REPOS_DIR /home/opnfv/repos
ENV QTIP_DIR /home/opnfv/repos/qtip
ENV PYTHONPATH /home/opnfv/repos/qtip
ENV HOME /home/opnfv
WORKDIR /home/opnfv


#Packaged Dependencies


RUN apt-get update && apt-get install -y \
software-properties-common \
wget \
git \
gcc \
ssh \
expect \
python-matplotlib \
python-dev \
python-pip \
libjpeg62 \
libjpeg62-dev \
zlib1g-dev \
python-tk \
curl \
supervisor \
--no-install-recommends

RUN apt-add-repository ppa:ansible/ansible -y
RUN apt-key update -y
RUN apt-get update -y
RUN apt-get install ansible --force-yes -y



RUN mkdir -p ${REPOS_DIR}
RUN mkdir -p /root/.ssh
RUN mkdir -p $HOME/qtip/logs
RUN chmod 700 /root/.ssh

#Config ansible
COPY ansible.cfg.default /root/.ansible.cfg

#Cloning Repos

RUN git config --global http.sslVerify false
RUN git clone https://gerrit.opnfv.org/gerrit/qtip $REPOS_DIR/qtip
RUN git clone https://gerrit.opnfv.org/gerrit/releng $REPOS_DIR/releng

RUN pip install -r $REPOS_DIR/qtip/requirements.txt

#Config supervisor

RUN mkdir -p /var/log/supervisor
RUN locale-gen en_US en_US.UTF-8
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf


CMD ["/usr/bin/supervisord"]
