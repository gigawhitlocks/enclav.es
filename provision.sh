#!/bin/bash

# update the system
echo "Starting full system update...";
yum update -y;
echo "Finished updating. Performing initial setup..";

# symlink the project directory somewhere more convenient
ln -s /vagrant/ /home/vagrant/cluster;

# install EPEL
echo "Installing EPEL..";
wget -q http://mirror.pnl.gov/epel/6/i386/epel-release-6-8.noarch.rpm \
	&& yum -y localinstall epel-release-6-8.noarch.rpm \
 	&& rm -f epel-release-6-8.noarch.rpm;

# disable EPEL repo by default
echo "Disabling EPEL by default.. (use with --enablerepo=epel)";
sed -i.bak s/enabled=1/enabled=0/g /etc/yum.repos.d/epel.repo;

# install pip
echo "Installing extra software from repos..";
yum install screen python-pip lsof expect -y --enablerepo=epel;

# install deps
pip-python install tornado redis jinja2 bulbs pytz;

# turns off selinux
echo 0 > /selinux/enforce;

echo "Installing & configuring firewall..";
# install apf & configure firewall
wget -q http://www.rfxn.com/downloads/apf-current.tar.gz;
tar xf apf-current.tar.gz;
cd apf-[0-9]*;
./install.sh;

# open port 1337
sed -i.bak s/IG_TCP_CPORTS=\"22\"/IG_TCP_CPORTS=\"22,1337\"/g /etc/apf/conf.apf \
		&& apf -r;

cd ..;
rm -f apf-current.tar.gz;

echo "Downloading Java..";
wget -q http://theknown.net/jdk-6u45-linux-x64-rpm.bin;

echo "Installing Java..";
chmod +x jdk-6u45-linux-x64-rpm.bin;
./jdk-6u45-linux-x64-rpm.bin;

echo "Downloading Neo4j..";
wget -q http://theknown.net/neo4j-community-1.8.1-unix.tar.gz;

echo "Installing Neo4j..";
tar xf neo4j-community-1.8.1-unix.tar.gz;
expect -c 'set timeout 20; spawn "./neo4j-community-1.8.1/bin/neo4j" install;\
	expect "*should run Neo4j?*" { send "\r" };\
	expect "*does not yet exist. Shall I create the account for you?*" { send "\r" };\
	interact;';

echo "Configuring system for Neo4j..";
ulimit -n 40000;
echo -e "\nneo4j   soft    nofile  40000\nneo4j   hard    nofile  40000\n" >> /etc/security/limits.conf
echo -e "\nsession    required   pam_limits.so\n" >> /etc/pam.d/su

echo "Starting neo4j...";
./neo4j-community-1.8.1/bin/neo4j start &

echo "All done!";
