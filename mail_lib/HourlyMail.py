import datetime
dt = lambda : str(datetime.datetime.now())[5:16]
import mailer

if __name__ == "__main__":
    mailer.send_email()