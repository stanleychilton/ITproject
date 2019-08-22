# ITproject

### Setup

1. Install boto3, and paramiko using the commands below in your command line.
   - `pip install boto3`
   - `pip install paramiko`
2. Install awscli.
    - for windows using [AWScli (64bit)](https://s3.amazonaws.com/aws-cli/AWSCLI64PY3.msi) / [AWScli (32bit)](https://s3.amazonaws.com/aws-cli/AWSCLI32PY3.msi)
    - for linux/mac the pip command `pip install awscli`
3. Run command `aws configure` in your command line and input your access key, security key ([shown on this page](https://console.aws.amazon.com/iam/home?#/users) by creating a user), and region.
4. Run python script `AutomaticEC2Creator.py` and select the csv file containing the students you want to create instances for.
