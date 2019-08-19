import smtplib, ssl

port = 587  # For SSL
smtp_server = "smtp.gmail.com"
sender_email = "codfisharecool987@gmail.com"  # Enter your address
receiver_email = "stanleychilton@live.com"  # Enter receiver address
password = "CodFish123"
message = """\
Subject: Massey 158.120 moodle link

Here is the link to your live version of moodle.
www.clicker-box.com"""

context = ssl.create_default_context()
with smtplib.SMTP(smtp_server, port) as server:
    server.ehlo()  # Can be omitted
    server.starttls(context=context)
    server.ehlo()  # Can be omitted
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, message)

