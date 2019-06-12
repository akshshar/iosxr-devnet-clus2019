#!/bin/bash

docker run -itd --restart=always --name openr --cap-add=SYS_ADMIN --cap-add=NET_ADMIN  -v /var/run/netns:/var/run/netns -v /misc/app_host:/root -v /misc/app_host/hosts_r2:/etc/hosts --hostname r2 192.168.122.11:5000/openr-xr /bin/bash -c "/root/       run_openr_r1.sh > /dev/null 2>&1"
