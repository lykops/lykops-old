安装过程以CentOS7.2为例：

1、关闭防火墙和selinux

    sed -i 's#SELINUX=enforcing#SELINUX=disabled#g' /etc/selinux/config
    for i in $(chkconfig --list|grep 3:on|awk '{print $1}' | egrep -v 'crond|network|rsyslog|sshd');do chkconfig --level 35 $i off;done 

2、安装依赖包

    yum install -y epel-release 
    yum install telnet ntpdate lrzsz bash glibc openssl vim automake autoconf gcc xz ncurses-devel patch python-devel git python-pip gcc-c++ redhat-rpm-config -y
    rpm -ivh http://dev.mysql.com/get/mysql57-community-release-el7-9.noarch.rpm
    yum install mysql-community-*  mysql-connector-python* --skip-broke
    yum upgrade -y

3、安装Python3

    wget https://www.python.org/ftp/python/3.5.2/Python-3.5.2.tgz -c
    tar zxvf Python-3.5.2.tgz 
    cd Python-3.5.2
    ./configure --prefix=/usr/local/python35 && make -j 5 && make install
    ln -sf /usr/local/python35/bin/* /bin/

4、下载代码到本地，进入根目录，执行

	pip3 install -r install/requirements.txt
    python35 ../manage.py makemigrations
    python35 ../manage.py migrate
	python35 ../manage.py runserver

5、安装nginx

    useradd nginx
    wget http://nginx.org/download/nginx-1.10.2.tar.gz
    tar zxvf nginx-1.10.2.tar.gz
    cd nginx-1.10.2
    ./configure --prefix=/usr/local/nginx && make -j 9 && make install

6、配置nginx

	/usr/local/nginx/conf/nginx.conf
	在server添加
    location / {
        proxy_redirect off;
        proxy_pass_header Server;
        proxy_set_header Host $http_host;
        proxy_set_header X-Scheme $scheme;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_pass http://localhost:8000;
    }
 	测试配置是否正常nginx -t
	没问题重启nginx
	
