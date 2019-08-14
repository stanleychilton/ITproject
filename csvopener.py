import csv, os, subprocess
# import the class definition from "email_handler.py" file
from email_handler import Class_eMail

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
                    subprocess.call(['sleep.sh', row[0], row[1], row[2], row[3]], shell=True)
                    line_count += 1

                    # set the email ID where you want to send the test email
                    To_Email_ID = row[3]

                    # Send Plain Text Email
                    email = Class_eMail()
                    email.send_Text_Mail(To_Email_ID, 'Plain Text Mail Subject',
                                         'This is sample plain test email body.')
                    del email
            print(f'Processed {line_count} lines.')
            break
    except Exception as e:
        print(e)