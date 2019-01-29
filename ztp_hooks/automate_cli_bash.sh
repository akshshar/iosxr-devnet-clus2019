#!/bin/bash

source /pkg/bin/ztp_helper.sh

declare -A loopback_addresses
declare -a rtr_list

rtr_list=("r1" "r2")
loopback_addresses["r1"]="50.1.1.1"
loopback_addresses["r2"]="60.1.1.1"

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
grpc
 service-layer
 port 57777
 no-tls
!
end
EOF

configure_xr /root/rtr_config
