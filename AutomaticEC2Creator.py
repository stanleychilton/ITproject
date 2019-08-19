import csv, os, subprocess
import boto3
import smtplib, ssl
ec2 = boto3.resource('ec2')
# import the class definition from "email_handler.py" file
students_list = []

port = 587  # For SSL
smtp_server = "smtp.gmail.com"
sender_email = "codfisharecool987@gmail.com"  # Enter your address
password = "CodFish123"



#Read number of lines and set up that many instances
with open(r'C:\Users\Admin\PycharmProjects\EC2Creator\test.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            print(f'Column names are {", ".join(row)}')
            line_count += 1
        else:
            print(row)
            line_count += 1
    print(f'Processed {line_count} lines.')

number_of_lines = line_count - 1


ec2 = boto3.resource('ec2')

instances = ec2.create_instances(
    ImageId='ami-082b5a644766e0e6f',
    MinCount=1,
    MaxCount=number_of_lines,
    InstanceType='t2.micro',
    KeyName='ec2-keypair'
)


files = os.listdir()
for x in range(0, len(files)):
    print(x+1, files[x])
while True:
    i = int(input("please choose a csv file to read: "))
    chosenfile = files[i-1]


    try:
        with open(chosenfile) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                if line_count == 0:
                    print(f'Column names are {", ".join(row)}')
                    line_count += 1
                else:
                    print(f'\t{row[0]} {row[1]} {row[2]} {row[3]}')
                    students_list.append([row[0], row[1], row[2], row[3]])
                    #subprocess.call(['sleep.sh', row[0], row[1], row[2], row[3]], shell=True)
                    # receiver_email = row[3]  # Enter receiver address
                    #
                    # message = """hello"""
                    #
                    # context = ssl.create_default_context()
                    # with smtplib.SMTP(smtp_server, port) as server:
                    #     server.ehlo()  # Can be omitted
                    #     server.starttls(context=context)
                    #     server.ehlo()  # Can be omitted
                    #     server.login(sender_email, password)
                    #     server.sendmail(sender_email, receiver_email, message)
                    line_count += 1
            print(f'Processed {line_count} lines.')
            break
    except Exception as e:
        print(e)

print(students_list)
l=[]
for i in ec2.instances.all():
    l.append(i.public_ip_address)
l = (list(filter(None, l)))
for i in students_list:
    i.append(l[0])
    l.pop(0)

print(students_list)

with open("output.csv",'w', newline='') as resultFile:
    wr = csv.writer(resultFile, dialect='excel')
    wr.writerows(students_list)