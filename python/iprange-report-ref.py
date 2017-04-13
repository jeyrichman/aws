#!/usr/bin/env python

import boto
from boto import ec2

Purple='\033[0;35m'
White='\033[0;37m'
Green='\033[0;32m'
Red = '\033[91m'
Yellow = '\033[93m'



def get_ec2_instances_groups():
    region=ec2.regions()
    for reg in region:
        connection=ec2.connect_to_region(reg.name)
        if reg.name == "us-gov-west-1" or reg.name == "cn-north-1":
            print Red + "API call is not allowed in this regions:",reg.name
            continue

        reservations=connection.get_all_reservations()
        sgs=connection.get_all_security_groups()
        if reservations:
                for reservation in reservations:
                        for instance in reservation.instances:
                                    print Green + "++++++ Found EC2 in region:",reg.name, "ID:" + Yellow + "%s" % (instance.id)
                for sg in sgs:
                    if len(sg.instances()) != 0:
                        print ("{0}\t{1}".format(sg.id, sg.name))
                        for rule in sg.rules:
                            print White + rule.ip_protocol, rule.from_port, rule.to_port, rule.grants
                        print ""
        else:
             print White + "Looking Instances in region:", reg.name, "..."

get_ec2_instances_groups()