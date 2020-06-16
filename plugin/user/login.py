from plugin import clientServer, Gmail, logo


class boneLogin():
    def __init__(self):
        self.account = ""
        self.password = ""

    def alert(self, msg):
        print("＊{}＊".format(msg))

    def loginForm(self):
        logo.login()
        self.alert("登入你的帳戶")
        self.account = input("帳號：")
        self.password = input("密碼：")
        data = {
            'act': 'login',
            'account': self.account,
            'password': self.password
        }
        cs = clientServer.client()
        result = cs.connect(1, data)
        if result[0] != None:
            logo.Welcome()
            self.alert('HI-{}'.format(result[0][2]))
        else:
            logo.loginFail()
        return result[0]


if __name__ == "__main__":
    test = boneLogin()
    test.loginForm()
