import smtplib
from email.mime.text import MIMEText
def Ginit():
    g = Gmail()
    return g
class Gmail:
    def __init__(self):
        self.gmail_user = ''  # 寄件者帳號
        self.gmail_password = ''  # 寄件者密碼(GOOGLE 應用程式密碼)

    def sendMsg(self, Subject="ErrorMsg", Content="content", to='asdewq45445@gmail.com'):
        msg = MIMEText(Content)
        msg['Subject'] = Subject
        msg['From'] = "BONEBLOG"
        msg['To'] = to
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(self.gmail_user, self.gmail_password)
        server.send_message(msg)
        server.quit()
        #print('[Info]Email sent!')
        #print('[Info]From:', self.gmail_user)
        #print('[Info]To:', to)
if __name__ == "__main__":
    g = Ginit()
    g.sendMsg()

