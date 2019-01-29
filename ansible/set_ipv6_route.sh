#!/bin/bash
for iface in $(/sbin/ip netns exec global-vrf /sbin/ifconfig | cut -d ' ' -f1| awk NF)
do
        if [[ $iface != *"lo"* ]] && [[ $iface != *"fwd_ew"* ]]; then
            /sbin/ip netns exec global-vrf /sbin/ip -6 route append fe80::/64 dev "$iface" proto kernel  metric 256
        fi
done
