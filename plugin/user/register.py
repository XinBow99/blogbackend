from plugin import clientServer, logo, Gmail


class boneRegister():
    def __init__(self):
        self.account = ""
        self.password = ""
        self.userName = ""
        self.nickname = ""
        self.school = ""
        self.email = ""

    def alert(self, msg):
        print("＊｜{}｜＊".format(msg))

    def registerForm(self):
        logo.register()
        self.alert("註冊一個帳戶")
        self.alert("＊為必填欄位")
        self.alert("＃＃＃＃＃＃＃＃＃＃")
        self.account = input("＊帳號：")
        self.password = input("＊密碼：")
        self.userName = input("＊姓名：")
        self.nickname = input("暱稱：")
        self.school = input("學校：")
        self.email = input("信箱：")
        data = {
            'act': 'register',
            'name': self.userName,
            'nickname': self.nickname,
            'account': self.account,
            'password': self.password,
            'school': self.school,
            'email': self.email,
        }
        cs = clientServer.client()
        status = cs.connect(
            0, data
        )
        g = Gmail.Ginit()
        g.sendMsg(
            "註冊骨頭部落格成功！！！",
            "恭喜你，快去發文吧！",
            self.email
        )
        return status


if __name__ == "__main__":
    test = boneRegister()
    test.registerForm()
