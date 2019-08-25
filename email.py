import csv, os
import smtplib, ssl


port = 587  # For SSL
smtp_server = "smtp.gmail.com"
sender_email = "codfisharecool987@gmail.com"  # Enter your address
password = "CodFish123"

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
                print(f'\t{row[0]} {row[1]} {row[2]} {row[3]} {row[4]}')
                receiver_email = row[3]  # Enter receiver address
                line_count += 1


                message = """\
Subject: Massey 158.120 moodle link
                
Here is the link to your live version of moodle.
""" + row[4]
                print(message)
                context = ssl.create_default_context()
                with smtplib.SMTP(smtp_server, port) as server:
                    server.ehlo()  # Can be omitted
                    server.starttls(context=context)
                    server.ehlo()  # Can be omitted
                    server.login(sender_email, password)
                    server.sendmail(sender_email, receiver_email, message)

            print(f'Processed {line_count} lines.')
            break
    except Exception as e:
        print(e)
