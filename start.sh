#!/usr/bin/bash -eu

mkdir -p log/
python3 setup/create_dockerfile.py
sudo docker image build -t dc-p0t/victim_con:1 .
sudo docker run -it -d -p 8080:80 --name victim dc-p0t/victim_con:1
sudo docker exec victim hostname -i
rm -f log/packet/tcpdump.pcap
mkdir -p log/packet
sudo tcpdump -i docker0 -s 0 -w log/packet/tcpdump.pcap &
sudo ./monitor/trace/tracer.py &>> log/ps_monitor.log &
echo -e "\n\n*** DC-p0t start !! ***\n"
