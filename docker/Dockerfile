##########################################
#####Docker container for QTIP############
##########################################


FROM ubuntu:14.04
MAINTAINER Nauman Ahad <Nauman_Ahad@dell.com>
LABEL version="0.1" description="OPNFV QTIP Docker container"




ENV repos_dir /home/opnfv/repos
WORKDIR /home/opnfv


#Packaged Dependencies


RUN apt-get update && apt-get install -y \
software-properties-common \
wget \
git \
gcc \
ssh \
expect \
python-dev \
python-pip \
--no-install-recommends

RUN apt-add-repository ppa:ansible/ansible -y
RUN apt-key update -y
RUN apt-get update -y
RUN apt-get install ansible --force-yes -y



RUN mkdir -p ${repos_dir}
RUN mkdir -p /root/.ssh
RUN chmod 700 /root/.ssh

#Cloning Repos

RUN git config --global http.sslVerify false
RUN git clone https://gerrit.opnfv.org/gerrit/qtip $repos_dir/qtip
RUN git clone https://gerrit.opnfv.org/gerrit/releng $repos_dir/releng

RUN pip install -r $repos_dir/qtip/docker/packages.pip


