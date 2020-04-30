import mailer
import datetime
today = datetime.datetime.today().date()

message = mailer.Message()

message.From = 'A30004560@agl.com.au'
message.To = ['javad.jazaeri@gmail.com, jjazaeri@agl.com.au']
message.Subject = 'DR BYOT churned customer report {0}'.format(today)

message.Body = '''Hi Team,

On {dt_today}, you got this email. 
'''.format(dt_today=today)
#message.attach("P:/New Energy/Churn Moveout Report/Input_file/Full VPPSA Site List V3.xlsx")

sender = mailer.Mailer('aglsmtp05.agl.com.au')

sender.send(message)
