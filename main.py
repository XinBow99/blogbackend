from plugin.user import register, login
from plugin.article import post
from plugin import logo


class A_User():
    def __init(self):
        self.userData = ""

    def choice(self, id=0):
        if id == 0:  # user Register and Login
            logo.choice()
            c = input("(1)註冊\n(2)登入\n快選一個：")
            if int(c) == 1:
                r = register.boneRegister()
                status = str(r.registerForm()[0])
                if status == "1":
                    self.choice(0)
            elif int(c) == 2:
                l = login.boneLogin()
                status = l.loginForm()
                if str(status) == "None":
                    self.choice(0)
                else:
                    self.userData = status
                    self.choice(1)
        # end of User
        # start of POST
        elif id == 1:
            p = post.articleAction(self.userData)
            p.listPosts()
            


if __name__ == "__main__":
    logo.screen()
    user = A_User()
    user.choice(0)
