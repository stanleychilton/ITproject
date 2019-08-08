#!/bin/bash
#### Description: Script to clone an EC2 instance with all its EBS volumes
#### Author: Michael Pietroforte, https://4sysops.com
#### Requirements: EC2 CLI tools, script only tested on OS X
#### License: Embrace and extend
 
#Set $id to the ID of the EC2 instance you want to clone
id=i-######## 
 
#Storing the description of the EC2 instance in a variable
instance_description=$(ec2-describe-instances $id)
 
#Reading the block devices of the instance; the cut command divides the string at the tab and extracts the second field
dev_list=$(echo "$instance_description" | grep BLOCKDEVICE | cut -f2 -d$'\t') 
#Storing the block devices in an array
devs=($dev_list) 
 
#Reading the EBS volumes of the instance
vol_list=$(echo "$instance_description" | grep BLOCKDEVICE | cut -f3 -d$'\t')
 
#Storing the volumes in an array
vols=($vol_list)
 
#Reading the instance type
instance_type=$(echo "$instance_description" | grep INSTANCE | cut -f10 -d$'\t')
 
#Reading the AWS region; the second grep command uses regex to remove the last digit because otherwise ec2-run-instance will fail
region=$(echo "$instance_description" | grep INSTANCE | cut -f12 -d$'\t' | grep -o -E '.*-.*-\d') 
 
#Reading the kernel ID
kernel=$(echo "$instance_description" | grep INSTANCE | cut -f13 -d$'\t')
 
#Reading the security group
security_group=$(echo "$instance_description" | grep RESERVATION | cut -f4 -d$'\t')
 
#Reading the key pair name
key=$(echo "$instance_description" | grep INSTANCE | cut -f7 -d$'\t') 
 
#Displaying the instance features
echo "Instance features:"
echo ""
echo "Block devices: ${devs[@]}"
echo "Volumes: ${vols[@]}"
echo "Instance type: $instance_type"
echo "Region: $region "
echo "Kernel ID: $kernel"
echo "Security group: $security_group"
echo "Key pair name: $key"
 
#Displaying the volumes with their features
echo ""
echo "Volumes found:"
 
let j=0 #Index for the volumes array
#Iterating through the volumes array to read the required features for the snapshots
for vol in "${vols[@]}"; do
 
    #Reading the volume features
    volumes=$(ec2-describe-volumes $vol)
 
    #Storing the volume sizes in an array
    vol_sizes[$j]=$(echo "$volumes" | grep VOLUME | awk '{print $3}')
 
    #Reading the volume types (gp2: general purpose (SSD), io1: provisioned IOPS (SSD), Not: standard magnetic)
    vol_types[$j]=$(echo "$volumes" | grep VOLUME | awk '{print $8}')
 
    #When we create the volume later, we have to omit the type for standard volumes
    if [ ${vol_types[$j]} == 'Not' ]; then
        vol_types[$j]=''
    fi
 
    #Reading the "Delete on Termination" setting; true if the volume will be deleted on instance termination, otherwise false
    vol_dels[$j]=$(echo "$volumes" | grep ATTACHMENT | awk '{print $7}')
 
    #Displaying the volume features
    echo ""
    echo "Volume id: " $vol
    echo "Size: "${vol_sizes[$j]}
    echo "Type: "${vol_types[$j]}
    echo "Delete on instance termination: "${vol_dels[$j]}
 
    #Creating a snapshot for each volume
    snapshots[$j]=$(ec2-create-snapshot $vol --region $region | awk '{print $2}')
 
    (( ++j ))
done
 
#We have to wait until all snapshots have been built so we can create the new volumes
echo ""
echo "Checking the status of the snapshots"
 
#Iterating through all snapshots in the array
for snapshot in "${snapshots[@]}"; do
    status=''
    until [ "$status" = "completed" ]; do
        status=$(ec2-describe-snapshots $snapshot | awk '{print $4}')
        echo "Snapshot: $snapshot Status: $status"
        sleep 5
    done
done
 
#We use the first snapshot for the AMI because it contains the root device; $ami stores the AMI ID, and we use the snapshot name as the AMI name
ami=$(ec2-register -n ${snapshots[0]} -s ${snapshots[0]} -architecture x86_64 --kernel $kernel | awk '{print $2}')
 
let l=0
#Iterating through the snapshots to create the --block-device-mapping parameter for the volumes we have to attach to the instance
for snapshot in "${snapshots[@]}"; do
    blockdevice=" -b ${devs[$l]}=${snapshots[$l]}:${vol_sizes[$l]}:${vol_dels[$l]}:${vol_types[$l]}"
    
    #Concatenating all parameters for the block devices
    blockdevices=$blockdevices$blockdevice
    (( ++l ))
done
 
#Creating the EC2 instance; if you want to add an ephemeral storage (if the instance type supports it), you can add something like this: -b "/dev/xvdb=ephemeral0" 
instance=$(ec2-run-instances $ami --region $region -k $key -g $security_group -t $instance_type $blockdevices)
 
#Reading the ID of the new instance
new_id=$(echo $instance | awk '{print $6}')
 
#Waiting until the instance is running and displaying its status
until [[ "$status" = *"running"* ]]; do
    status=$(ec2-describe-instances $new_id | awk '{print $6}')
    echo ""
    echo "Instance status: $status"
    sleep 5
done
 
#Reading the public IP address so we can connect to the instance
ip=$(ec2-describe-instances $new_id | awk '{print $14}')
echo ""
echo "Instance IP address: $ip"