#!/bin/bash
#Check available EC2 instances in AWS Regions

Purple='\033[0;35m'
White='\033[0;37m'        
Green='\033[0;32m'   
Yellow='\033[93m'

LISTREGIONS=`aws ec2 describe-regions --query 'Regions[*].RegionName' --output text`
INDEX=0
for region in $LISTREGIONS;
do
                EC2ID=`aws ec2 describe-instances --region $region --query 'Reservations[*].Instances[*].InstanceId' --output text`
                if [[ -z "${EC2ID// }" ]]; then
                        echo -e $White"Looking Instances in region: "$region...$EC2ID
                else
                        echo -e $Green ++++++ Found EC2 in region: $region, ID:$Yellow$EC2ID
                        GROUPID=`aws ec2 describe-instances  --region $region --instance-ids $EC2ID --query 'Reservations[*].Instances[*].SecurityGroups[*].GroupId'  --output text`
                        echo -e $White =================================
                        echo -e $Purple REGION '=>' $region;
                        for group in $GROUPID;do
                                echo -e $Purple "    SG => $group"
                                echo -e $White "FROM   TO      IP"
                                aws ec2 describe-security-groups --region $region  --group-ids $group --query "SecurityGroups[*].IpPermissions[*].[FromPort,ToPort,join(',',IpRanges[*].CidrIp)]"  --output text
                                RULES[$INDEX]=`aws ec2 describe-security-groups --region $region  --group-ids $group --query "SecurityGroups[*].IpPermissions[*].[FromPort,ToPort,join(',',IpRanges[*].CidrIp)]"  --output text | awk '{print$3}'| sort -u | uniq`         
                                let INDEX=${INDEX}+1;
                                echo "";
                        done
                fi
done

for ip in ${RULES[@]};do
        IP=`echo $ip | cut -d\/ -f1`
        ORG=`whois $IP | grep 'OrgName'`
        PRINT=`echo -e $Green $IP $Purple '=>' $White $ORG`
        echo $PRINT && echo  $PRINT >> info.csv
done

echo ""
echo "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
echo "Information about all IP Subnets been written to info.csv"
echo "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
