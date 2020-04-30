import sys
def job_email(user, reciever_emails):
  import mailer
  import datetime
  today = datetime.datetime.today().date()

  message = mailer.Message()

  message.From = '{user}@agl.com.au'.format(user=user)
  message.To = [reciever_emails]
  message.Subject = 'DR BYOT churned customer report {0}'.format(today)

  message.Body = '''Hi Team,

  On {dt_today}, you got this email. 
  '''.format(dt_today=today)
  #message.attach("P:/New Energy/Churn Moveout Report/Input_file/Full VPPSA Site List V3.xlsx")

  sender = mailer.Mailer('aglsmtp05.agl.com.au')

  sender.send(message)
  return()
if __name__ == '__main__':
    user = sys.argv[1]
    reciever_emails = sys.argv[2]
    job_email(user=user, reciever_emails=reciever_emails)
