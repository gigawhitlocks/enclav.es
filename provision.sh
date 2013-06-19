#!/bin/bash


# install java
apt-get install python-software-properties make python-dev protobuf-compiler -y -q;
add-apt-repository ppa:webupd8team/java;
apt-get update -y -q;
apt-get install oracle-java6-installer -y;


# symlink the project directory somewhere more convenient
ln -s /vagrant/ /home/vagrant/enclav.es;

##############
#INSTALL REQUIRED PACKAGES
##############
apt-get install sendmail git zip python-pip screen make bpython expect -y -q;

##############
#INSTALL PYTHON DEPS.
#IF NEW DEPS ARE INSTALLED OR REMOVED AFTER INSTALLATION/REMOVAL DO
#pip freeze > /home/vagrant/enclav.es/requirements.txt
#AND COMMIT NEW CHANGES TO KEEP TRACK OF THESE DEPENDENCIES
#############
pip install -r /home/vagrant/enclav.es/requirements.txt

wget http://s3.thinkaurelius.com/downloads/titan/titan-all-0.3.1.zip
unzip titan-all-0.3.1.zip

# Download riak

wget http://s3.amazonaws.com/downloads.basho.com/riak/1.3/1.3.1/ubuntu/precise/riak_1.3.1-1_amd64.deb
dpkg -i riak_1.3.1-1_amd64.deb
cp -f /vagrant/app.config /etc/riak/app.config
