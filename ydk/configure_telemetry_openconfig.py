#!/usr/bin/env python
#
# Copyright 2016 Cisco Systems, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

"""
Create configuration for model openconfig-telemetry.

usage: configure_telemetry_openconfig.py [-h] [-v] device

positional arguments:
  device         NETCONF device (ssh://user:password@host:port)

optional arguments:
  -h, --help     show this help message and exit
  -v, --verbose  print debugging messages
"""

from argparse import ArgumentParser
from urlparse import urlparse

from ydk.services import CRUDService
from ydk.providers import NetconfServiceProvider
from ydk.models.openconfig import openconfig_telemetry \
    as oc_telemetry
import logging


def config_telemetry_system(telemetry_system):
    """Add config data to telemetry_system object."""
    #sensor-group
    sensor_group = telemetry_system.sensor_groups.SensorGroup()


    sensor_group.sensor_group_id = "BGPSession"

    sensor_path = sensor_group.sensor_paths.SensorPath()
    sensor_path.path = "Cisco-IOS-XR-ipv4-bgp-oper:bgp/instances/instance/instance-active/default-vrf/sessions"
    sensor_group.sensor_paths.sensor_path.append(sensor_path)
    telemetry_system.sensor_groups.sensor_group.append(sensor_group)

    sensor_path = sensor_group.sensor_paths.SensorPath()
    sensor_path.path = "Cisco-IOS-XR-ipv4-bgp-oper:bgp/instances/instance/instance-active/default-vrf/process-info"
    sensor_group.sensor_paths.sensor_path.append(sensor_path)
    telemetry_system.sensor_groups.sensor_group.append(sensor_group)


    sensor_group = telemetry_system.sensor_groups.SensorGroup()
    sensor_group.sensor_group_id = "IPV6Neighbor"

    sensor_path = sensor_group.sensor_paths.SensorPath()
    sensor_path.path = "Cisco-IOS-XR-ipv6-nd-oper:ipv6-node-discovery/nodes/node/neighbor-interfaces/neighbor-interface/host-addresses/host-address"
    sensor_group.sensor_paths.sensor_path.append(sensor_path)
    telemetry_system.sensor_groups.sensor_group.append(sensor_group)


    #subscription
    subscription = telemetry_system.subscriptions.persistent.Subscription()
    subscription.subscription_id = 1
    sensor_profile = subscription.sensor_profiles.SensorProfile()
    sensor_profile.sensor_group = "BGPSession"
    sensor_profile.config.sensor_group = "BGPSession"
    sensor_profile.config.sample_interval = 15000
    subscription.sensor_profiles.sensor_profile.append(sensor_profile)
    telemetry_system.subscriptions.persistent.subscription.append(subscription)

    subscription = telemetry_system.subscriptions.persistent.Subscription()
    subscription.subscription_id = 2
    sensor_profile = subscription.sensor_profiles.SensorProfile()
    sensor_profile.sensor_group = "IPV6Neighbor"
    sensor_profile.config.sensor_group = "IPV6Neighbor"
    sensor_profile.config.sample_interval = 15000
    subscription.sensor_profiles.sensor_profile.append(sensor_profile)
    telemetry_system.subscriptions.persistent.subscription.append(subscription)

if __name__ == "__main__":
    """Execute main program."""
    parser = ArgumentParser()
    parser.add_argument("-v", "--verbose", help="print debugging messages",
                        action="store_true")
    parser.add_argument("device",
                        help="NETCONF device (ssh://user:password@host:port)")
    args = parser.parse_args()
    device = urlparse(args.device)

    # log debug messages if verbose argument specified
    if args.verbose:
        logger = logging.getLogger("ydk")
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        formatter = logging.Formatter(("%(asctime)s - %(name)s - "
                                      "%(levelname)s - %(message)s"))
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    # create NETCONF provider
    provider = NetconfServiceProvider(address=device.hostname,
                                      port=device.port,
                                      username=device.username,
                                      password=device.password,
                                      protocol=device.scheme)
    # create CRUD service
    crud = CRUDService()

    telemetry_system = oc_telemetry.TelemetrySystem()  # create object
    config_telemetry_system(telemetry_system)  # add object configuration

    # create configuration on NETCONF device
    crud.create(provider, telemetry_system)

    exit()
# End of script
