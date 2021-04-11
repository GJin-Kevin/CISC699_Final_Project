import smtplib
from email.message import EmailMessage

class Notification():

    def __init__(self, email_add, email_password, mail_server: str = 'gmail'):
        """[summary] Initialize an instance of Notification.

        Args:
            email_add ([type]): [Email address]
            email_password ([type]): [Email password]
            mail_server (str, optional): [Email server]. Defaults to 'gmail'.
        """        
        self.mail_server = mail_server
        self.email_add = email_add
        self.email_pw = email_password

    def send_buy_notification(self, send_to:str, sec_id):
        """[summary] Send an email notification

        Args:
            send_to (str): [Email address to send to]
        """        
        
        if self.mail_server == 'gmail':

            msg = EmailMessage()
            msg['Subject'] = '[CATA] New Message - Buy Alert'
            msg['From'] = self.email_add
            msg['To'] = send_to
            msg.set_content('BUY Signal: Stoct {} . A market BUY order has been submitted to Interactive Broker. Please review.'.format(sec_id))

            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login(self.email_add, self.email_pw)
                smtp.send_message(msg)

    def send_sell_notification(self, send_to:str, sec_id):
        """[summary] Send an email notification

        Args:
            send_to (str): [Email address to send to]
        """        
        
        if self.mail_server == 'gmail':

            msg = EmailMessage()
            msg['Subject'] = '[CATA] New Message - Sell Alert'
            msg['From'] = self.email_add
            msg['To'] = send_to
            msg.set_content('SELL Signal: Stoct {} . A market SELL order has been submitted to Interactive Broker. Please review.'.format(sec_id))

            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login(self.email_add, self.email_pw)
                smtp.send_message(msg)
