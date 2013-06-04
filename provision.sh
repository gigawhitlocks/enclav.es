#!/bin/bash


# install java
apt-get install python-software-properties make -y -q;
add-apt-repository ppa:webupd8team/java;
apt-get update -y -q;
apt-get install oracle-java6-installer -y;


# symlink the project directory somewhere more convenient
ln -s /vagrant/ /home/vagrant/cluster;
apt-get install python-dev swig python-pip screen make ipython expect -y -q;
pip install -r /home/vagrant/cluster/requirements.txt

echo "Downloading Neo4j..";
cd /opt;
wget https://dl.dropboxusercontent.com/u/14943993/neo4j-community-1.8.1-unix.tar.gz;

echo "Installing Neo4j..";
tar xf neo4j-community-1.8.1-unix.tar.gz;
useradd neo4j;

ulimit -n 40000;
echo "Starting neo4j...";
chown -R neo4j.neo4j /opt/neo4j-community-1.8.1;
/opt/neo4j-community-1.8.1/bin/neo4j start;
cd /home/vagrant/;

# Download redis

echo "Installing redis..";
wget https://dl.dropboxusercontent.com/u/14943993/redis-2.6.9.tar.gz;
tar xf redis-[0-9]*;
cd redis-[0-9]*;
make;
make install;
sysctl vm.overcommit_memory=1;
echo "vm.overcommit_memory = 1" >> /etc/sysctl.conf

# set redis to run in background & then run redis
sed -i.bak 's/daemonize no/daemonize yes/g' /home/vagrant/redis-[0-9]*/redis.conf
/usr/local/bin/redis-server /home/vagrant/redis-[0-9]*/redis.conf &

