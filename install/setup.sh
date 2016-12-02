#!/bin/bash
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:

setenforce 0
service iptables stop

sed -i 's#SELINUX=enforcing#SELINUX=disabled#g' /etc/selinux/config
for i in $(chkconfig --list|grep 3:on|awk '{print $1}' | egrep -v 'crond|network|rsyslog|sshd');do chkconfig --level 35 $i off;done 
yum install -y epel-release 
yum install telnet ntpdate lrzsz bash glibc openssl vim automake autoconf gcc xz ncurses-devel patch python-devel git python-pip gcc-c++ redhat-rpm-config -y

rpm -ivh http://dev.mysql.com/get/mysql57-community-release-el7-9.noarch.rpm
yum install mysql-community-*  mysql-connector-python* --skip-broke

yum upgrade -y

pip3 install -r requirements.txt

wget https://www.python.org/ftp/python/3.5.2/Python-3.5.2.tgz -c
tar zxvf Python-3.5.2.tgz 
cd Python-3.5.2
./configure --prefix=/usr/local/python35 && make -j 5 && make install
ln -sf /usr/local/python35/bin/* /bin/
/usr/local/py34/bin/python35 ../manage.py makemigrations
/usr/local/py34/bin/python35 ../manage.py migrate


useradd nginx
wget http://nginx.org/download/nginx-1.10.2.tar.gz
tar zxvf nginx-1.10.2.tar.gz
cd nginx-1.10.2
./configure --prefix=/usr/local/nginx && make -j 9 && make install 
