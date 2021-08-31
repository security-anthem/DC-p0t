def write_dockerfile(app, version):
    if app == "apache":
        write_apache_dockerfile(version)
        return 0
    elif app == "bind9":
        write_bind_dockerfile(version)
        return 0
    elif app == "php":
        write_php_dockerfile(version)
        return 0
    else:
        print("Invalid value:", app)
        return 1

def write_apache_dockerfile(version):
    with open('Dockerfile', mode='w') as f:
        f.write('FROM ubuntu\n')
        f.write('LABEL maintainer="dc-p0tter"\n')
        f.write('RUN apt-get update && apt-get install -y tzdata\n')
        f.write('ENV TZ=Asia/Tokyo\n')
        f.write('RUN apt-get update && apt-get install -y wget ')
        f.write('libapr1-dev ')
        f.write('libaprutil1-dev ')
        f.write('build-essential ')
        f.write('libpcre3-dev\n')
        f.write('RUN wget https://archive.apache.org/dist/httpd/httpd-')
        f.write(version)
        f.write('.tar.gz\n')
        f.write('RUN tar xvf httpd-')
        f.write(version)
        f.write('.tar.gz\n')
        f.write('WORKDIR /httpd-')
        f.write(version)
        f.write('\n')
        f.write('RUN ./configure --prefix=/usr/local/apache2 && make && make install\n')
        f.write('EXPOSE 80\n')
        f.write('CMD ["/usr/local/apache2/bin/apachectl", "-DFOREGROUND"]\n')

def write_bind_dockerfile(version):
    with open('Dockerfile', mode='w') as f:
        f.write('FROM ubuntu\n')
        f.write('LABEL maintainer="dc-p0tter"\n')
        f.write('RUN apt-get update && apt-get install -y tzdata\n')
        f.write('ENV TZ=Asia/Tokyo\n')
        f.write('RUN apt-get update && apt-get install -y git autoconf libtool automake pkg-config python3 python3-ply libuv1-dev libssl-dev libcap-dev wget\n')
        f.write('RUN git clone https://gitlab.isc.org/isc-projects/bind9.git && cd bind9 && git checkout ')
        f.write(version)
        f.write('\nWORKDIR /bind9 \n')
        f.write('RUN autoreconf -fi && ./configure && make && make install\n')
        f.write('COPY ./etc/bind_config/* /usr/local/etc/\n')
        f.write('RUN mkdir -p /var/cache/bind\n')
        f.write('RUN mkdir -p /usr/share/dns\n')
        f.write('RUN wget ftp://rs.internic.net/domain/named.cache -P /usr/share/dns\n')
        f.write('EXPOSE 53\n')
        f.write('CMD ["named", "-g"]\n')

def write_php_dockerfile(version):
    with open('Dockerfile',mode='w') as f:
        f.write('FROM ubuntu\n')
        f.write('LABEL maintainer="dc-p0tter"\n')
        f.write('RUN apt-get update && apt-get install -y tzdata\n')
        f.write('ENV TZ=Asia/Tokyo\n')
        f.write('RUN apt-get update && apt-get install -y wget libapr1-dev  libaprutil1-dev build-essential\n')
        f.write('RUN apt-get update && apt-get install -y libpcre3-dev libxml2-dev sqlite3 libsqlite3-dev libonig-dev pkg-config zlib1g-dev\n')
        f.write('RUN wget https://archive.apache.org/dist/httpd/httpd-2.2.18.tar.gz\n')
        f.write('RUN tar xvzf httpd-2.2.18.tar.gz\n')
        f.write('RUN wget https://www.php.net/distributions/php-')
        f.write(version)
        f.write('.tar.gz\n')
        f.write('RUN tar xvzf php-')
        f.write(version)
        f.write('.tar.gz\n')
        f.write('WORKDIR /httpd-2.2.18\n')
        f.write('RUN ./configure --prefix=/usr/local/apache2 && make && make install\n')
        f.write('WORKDIR /php-')
        f.write(version)
        f.write('\n')
        f.write('RUN ./configure --with-apxs2=/usr/local/apache2/bin/apxs --with-mysqli --with-pdo-mysql --enable-mbregex --enable-mbstring\n')
        f.write('RUN make && make install\n')
        f.write('COPY etc/php.ini /usr/local/lib/\n')
        f.write('COPY etc/httpd.conf /usr/local/apache2/conf/\n')
        f.write('COPY etc/phpi.php /usr/local/apache2/htdocs/\n')
        f.write('WORKDIR /var/www/html\n')
        f.write('EXPOSE 80\n')
        f.write('#start apache\n')
        f.write('CMD ["/usr/local/apache2/bin/apachectl", "-DFOREGROUND"]\n')
