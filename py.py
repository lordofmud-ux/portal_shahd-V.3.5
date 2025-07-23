from sendgrid.models import Email

smtp_server = "smtp.gmail.com"
sender_email = 'shahdgroup.portal@gmail.com'
port = 465
receiver_email = 'aliizadi208@gmail.com'
message = 'Salam'
password = '32fgy78uh3hh3f4'


import smtplib, ssl

port = 465  # For SSL
smtp_server = "smtp.gmail.com"
sender_email = 'shahdgroup.portal@gmail.com'  # Enter your address
receiver_email = 'aliizadi208@gmail.com'  # Enter receiver address
password = '32fgy78uh3hh3f4'
message = 'Salam'


import smtplib
s = smtplib.SMTP('smtp.gmail.com', 587)
s.starttls()
s.login('shahdgroup.portal@gmail.com', '32fgy78uh3hh3f4')
message = 'Salam'
s.sendmail('shahdgroup.portal@gmail.com', 'aliizadi208@gmail.com', message)
s.quit()
