#!/bin/bash

docker run -itd --restart=always --name openr --cap-add=SYS_ADMIN --cap-add=NET_ADMIN  -v /var/run/netns:/var/run/netns -v /misc/app_host:/root -v /misc/app_host/hosts_r2:/etc/hosts --hostname r2 akshshar/openr-xr /root/run_openr_r2.sh
