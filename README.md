# ITproject

### Description

This script creates one ec2 instance and installs moodle onto it. Once that has completed the image is shapshotted. The script then sets up as many instances as there are students in the class, all with moodle installed on them.
the instances are created along side a security group which opens the instances for connection through a browser so that the student can view their instance.  


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
5. Change the url variable in NewCreator.py and instance.py from our testing site to your own link if you have set one up
6. Run python script `NewCreator.py`(this will complete the setup for every instance).
7. Once the instance are set up and you are ready for the students to access their sites yuo need to allow all traffic on the default security group. This is done by right clicking on the default security group ([shown on the page](https://us-west-2.console.aws.amazon.com/ec2/v2/home?region=us-west-2#SecurityGroups:sort=desc:tag:Name)) and selecting edit inbound rules. Once this is done select add rule and change the Type to "all traffic".
8. When ready to give students the urls email them the link to the website we have created. Here they will be able to select there instance and alos throughout the semester be able to tell if their instance is running with our system operation status script.
