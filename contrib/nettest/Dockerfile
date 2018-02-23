########################################################## 
# Dockerfile to run a flask-based web application# Based on an ubuntu:16.04 
##########################################################

# Set the base image to use to centos 
FROM ubuntu:16.04

# Set the file maintainer 
MAINTAINER Qiang.Dai@spirent.com

# Set env varibles used in this Dockerfile (add a unique prefix, such as DOCKYARD) 
# Local directory with project source 
ENV DOCKYARD_SRC=nettest 
# Directory in container for all project files 
ENV DOCKYARD_SRCHOME=/opt 
# Directory in container for project source files 
ENV DOCKYARD_SRCPROJ=/opt/nettest

# Update the defualt application repository source list 
#RUN yum -y install epel-release 
#RUN yum -y install python-pip 
#RUN yum clean all
RUN apt-get update && apt-get install -y \
 python-pip

# Copy application source code to SRCDIR 
COPY $DOCKYARD_SRC $DOCKYARD_SRCPROJ

# Create application subdirectories 
WORKDIR $DOCKYARD_SRCPROJ 
RUN mkdir log 
VOLUME [“$DOCKYARD_SRCPROJ/log/”]

# Install Python dependencies 
RUN pip install -r $DOCKYARD_SRCPROJ/requirements.txt

# Port to expose 
EXPOSE 5000

# Copy entrypoint script into the image 
WORKDIR $DOCKYARD_SRCPROJ

#CMD ["/bin/bash"]
CMD ["/bin/bash", "start.sh"]
#ENTRYPOINT  ["/usr/bin/python /opt/nettest/rest_server.py"] 
#ENTRYPOINT [“./start_server.sh”]
#ENTRYPOINT [“/bin/bash”]
