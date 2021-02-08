#!/usr/bin/bash -eu

mkdir -p var/log/
python3 setup/create_dockerfile.py
sudo docker image build -t dc-p0t/victim_con:1 .
sudo docker run -it -d -p 8080:80 --name victim dc-p0t/victim_con:1
sudo docker exec victim hostname -i
rm -f var/log/packet/tcpdump.pcap
mkdir -p var/log/packet
sudo tcpdump -i docker0 -s 0 -w var/log/packet/tcpdump.pcap &
echo -e "\n\n*** DC-p0t start !! ***\n"
