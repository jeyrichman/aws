#!/usr/bin/env python

import boto
from boto import ec2

Purple='\033[0;35m'
White='\033[0;37m'
Green='\033[0;32m'
Red = '\033[91m'
Yellow = '\033[93m'


def get_ec2_instances():
    region=ec2.regions()
    for reg in region:
        connection=ec2.connect_to_region(reg.name)
        if reg.name == "us-gov-west-1" or reg.name == "cn-north-1":
            print Red + "API call is not allowed in this regions:",reg.name
            continue

        reservations=connection.get_all_reservations()
        if reservations:
                print Green + "++++++ Found EC2 in region:",reg.name, "..."
                for reservation in reservations:
                        for instance in reservation.instances:
                                    print Yellow + "%s" % (instance.id)
        else:
             print White + "Looking Instances in region:", reg.name, "..."

get_ec2_instances()