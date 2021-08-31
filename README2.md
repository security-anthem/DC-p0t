# DC-p0t

Vulnerability verification

Honeypot on Docker container

## env

Ubuntu 20.10 (Linux 5.8.0-33-generic)

VirtualBox 6.1.16

## Usage

### packages

1. eBPFのインストール

```
$ sudo apt update
$ sudo apt install -y bpfcc-tools
```

2. Dockerのインストール
 
https://docs.docker.com/engine/install/ubuntu/

### start

```
$ ./start.sh
```

1. write Dockerfile
2. create Docker container
3. run tcpdump

### stop

```
$ ./stop.sh
```

## Related Works

honeytrap

https://github.com/honeytrap/honeytrap
