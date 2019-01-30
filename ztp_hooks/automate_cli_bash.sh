#!/bin/bash

source /pkg/bin/ztp_helper.sh

declare -A loopback_addresses
declare -A gig0_ipv4_address
declare -A gig1_ipv4_address
declare -A gig2_ipv4_address
declare -a rtr_list

rtr_list=("r1" "r2")
loopback_addresses["r1"]="50.1.1.1"
loopback_addresses["r2"]="60.1.1.1"

gig0_ipv4_address["r1"]="10.1.1.10"
gig0_ipv4_address["r2"]="10.1.1.20"

gig1_ipv4_address["r1"]="11.1.1.10"
gig1_ipv4_address["r2"]="11.1.1.20"

gig2_ipv4_address["r1"]="12.1.1.10"
gig2_ipv4_address["r2"]="12.1.1.20"



function configure_xr()
{
   config_file=$1

   xrapply $config_file

   if [[ $? == 1 ]];then
       config_failed=`xrcmd "show configuration failed"`
       echo "$config_failed"
   else
       config_success=`xrcmd "show configuration commit changes last 1"`
       echo "$config_success"
   fi
}

function get_hostname()
{
    hostname_config=`xrcmd "show running-config hostname"`
    hostname=`echo $hostname_config | cut -d " " -f 2`
}


get_hostname

cat > /root/rtr_config << EOF
!
interface Loopback0
  ipv4 address ${loopback_addresses[${hostname}]}/32
  !
!
interface GigabitEthernet0/0/0/0
  no shutdown
  ipv6 enable
  ipv4 address ${gig0_ipv4_address[${hostname}]}/24
  !
!
interface GigabitEthernet0/0/0/1
  no shutdown
  ipv6 enable
  ipv4 address ${gig1_ipv4_address[${hostname}]}/24
  !
!
interface GigabitEthernet0/0/0/2
  no shutdown
  ipv6 enable
  ipv4 address ${gig2_ipv4_address[${hostname}]}/24
  !
!
grpc
 service-layer
 port 57777
 no-tls
!
end
EOF

configure_xr /root/rtr_config
