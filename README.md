# ITproject

### Description

This script creates an EC2 instance for every student in a csv file (comma delimited) and then ssh's into it and installs moodle, mysql, apache webserver.
the instances are created along side a security group which opens the instances for connection through a browser so that the student can view their instance. After all instances are created the student and their assigned url are saved into a output csv file which when all instances are working and moodle is installed. 
This means every student can be emailed their url at the click of one button when the teacher or linux admin is ready.

**(installation guide below)**


---


### Required software

1. **python 3**
2. **AWScli** (install guide below) 
3. **boto3** for python (install guide below)
4. **paramiko** for python (install guide below)

---

### Setup

1. Install boto3, and paramiko using the commands below in your command line.
   - `pip install boto3`
   - `pip install paramiko`
2. Install awscli.
    - for windows using [AWScli (64bit)](https://s3.amazonaws.com/aws-cli/AWSCLI64PY3.msi) / [AWScli (32bit)](https://s3.amazonaws.com/aws-cli/AWSCLI32PY3.msi)
    - for linux/mac the pip command `pip install awscli`
3. Change the gmail address and password settings in the ______ file and turn on Less secure app access [here](https://myaccount.google.com/u/3/lesssecureapps?utm_source=google-account&utm_medium=web)
4. Run command `aws configure` in your command line and input your access key, security key ([shown on this page](https://console.aws.amazon.com/iam/home?#/users) by creating a user), and region.
5. Run python script `AutomaticEC2Creator.py` and select the csv file containing the students you want to create instances for (this will complete the setup for every instance).
6. Once the instance are set up and you are ready for the students to access their sites yuo need to allow all traffic on the default security group. This is done by right clicking on the default security group ([shown on the page](https://us-west-2.console.aws.amazon.com/ec2/v2/home?region=us-west-2#SecurityGroups:sort=desc:tag:Name)) and selecting edit inbound rules. Once this is done select add rule and change the Type to "all traffic".
7. When ready to give students the urls to their instances run the `email.py` which will send an email to every user with the url.
