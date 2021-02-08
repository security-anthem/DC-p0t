def write_dockerfile(app, version):
    if app == "apache":
        write_apache_dockerfile(version)
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
