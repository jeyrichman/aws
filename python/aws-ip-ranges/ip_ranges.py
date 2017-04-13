import os
from pprint import pprint

import boto3
from ipwhois import IPWhois

access_key = os.environ['ACCESS_KEY']
secret_key = os.environ['SECRET_KEY']


def get_range(rule):
    start_port = rule.get('FromPort', 0)
    end_port = rule.get('ToPort', 65535)
    cidr_ip = frozenset([range['CidrIp'] for range in rule['IpRanges']])
    return cidr_ip, "{}-{}".format(start_port, end_port)


def whois_enrich_and_pretty_print(ip_range):

    def whois_info(sidr):
        try:
            lk = IPWhois(sidr)
            return lk.lookup_whois()
        except Exception as e:
            return ''

    subnets_ranges = []
    for sidr in ip_range[0]:
        splitted_sidr = sidr.split('/')
        if splitted_sidr[1] != '0':
            subnets_ranges.append({'ip_range': sidr, 'whois_info': whois_info(splitted_sidr[0])})
        pprint({'Ports range': ip_range[1],
                'Ip ranges': subnets_ranges
                })


def get_ranges():

    session = boto3.Session(
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key
    )

    ec2 = session.resource('ec2')
    instances = ec2.instances.all()
    rules = sum([ec2.SecurityGroup(group['GroupId']).ip_permissions for inst
                 in instances for group in inst.security_groups], [])
    ip_ranges = set(map(get_range, rules))

    for r in ip_ranges:
        whois_enrich_and_pretty_print(r)

if __name__ == "__main__":
    get_ranges()
