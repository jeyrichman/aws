import boto
from boto import ec2

from ipwhois import IPWhois
import pprint
import csv

Purple='\033[0;35m'
White='\033[0;37m'
Green='\033[0;32m'
Red = '\033[91m'
Yellow = '\033[93m'



def whois_info(sidr):
    out = open('out.csv', 'a')
    lk = IPWhois(unicode(sidr))
    results = lk.lookup_whois()
    pprint.pprint(results, stream=out)
    out.close()



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
                            instance=instance.id
                for sg in sgs:
                    if len(sg.instances()) != 0:
                        for rule in sg.rules:
                            splitted_sidr=str(rule.grants[0])
                            if splitted_sidr[-1:] != '0':
                                print Green + "++++++ Found EC2 in region:",reg.name + "\n" + Red + "InstanceID: " + Yellow + "%s" % (instance) + \
                                "\n" + Red + "IP: " + Green, splitted_sidr[:-1-2], White + "=>" + Purple + " [" + rule.from_port + "]", "[" + rule.to_port + "]" + \
                                "\n" + Red + "Whois Info: writed to './out.csv' file" + White
                                whois_info(splitted_sidr[:-1-2])
                                print ""
        else:
             print White + "Looking Instances in region:", reg.name, "..."


def clearCSV():
    with open('out.csv', "w"):
        pass

if __name__ == "__main__":
    clearCSV()
    get_ec2_instances_groups()
    print 'All information about subnets saved to out.csv file. Please check'