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
cat /etc/yum.repos.d/epel.repo | sed -e s/enabled=1/enabled=0/g > epel2.repo \
	&& mv -f epel2.repo /etc/yum.repos.d/epel.repo;

# install pip
echo "Installing PIP, screen, & Python deps..";
yum install screen python-pip -y --enablerepo=epel;

# install deps
pip-python install tornado redis jinja2 bulbs pytz;

# turns off selinux
echo 0 > /selinux/enforce;

# turns off the firewall TODO: REMOVE THIS AND SET UP THE FIREWALL FO REALZ
/etc/init.d/iptables stop;

