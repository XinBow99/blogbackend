import time
from os import system, name


def clear():
    time.sleep(0.1)
    if name == 'nt':
        system('cls')
    else:
        system('clear')


def press(txt):
    hashTag = "＃"
    finalTag = ""
    for tag in range(0, int(len(txt.split('\n')[0])/2) + 2):
        str(tag)
        finalTag += hashTag
    return "{}\n{}\n{}".format(finalTag, txt, finalTag)


def getTxt(txt, *args):
    hashTag = "＃"
    finalTag = ""
    for tag in range(0, int(len(txt.split('\n')[0])/2) + 2):
        str(tag)
        finalTag += hashTag
    for i, arg in enumerate(args):
        if i + 1 != len(args):
            txt += arg + '\n'
        else:
            txt += arg
    clear()
    return "{}\n{}\n{}".format(finalTag, txt, finalTag)


def screen():
    with open('./plugin/logos/Welcome.txt', 'r', encoding='utf8') as l:
        print(getTxt(l.read(),
                     "Tips:此部落格目前使用Python實作，未來會使用網頁版"))
        l.close()
    with open('./plugin/logos/Pressenter.txt', 'r', encoding='utf8') as l:
        print(press(l.read()))
        l.close()
        input()


def register():
    with open('./plugin/logos/register.txt', 'r', encoding='utf8') as l:
        print(getTxt(l.read(),
                     "Tips:在這裡註冊一個溫暖的帳號"
                     ))
        l.close()


def login():
    with open('./plugin/logos/login.txt', 'r', encoding='utf8') as l:
        print(getTxt(l.read(),
                     "Tips:快登入來找骨頭聊天"
                     ))
        l.close()


def loginFail():
    with open('./plugin/logos/loginfail.txt', 'r', encoding='utf8') as l:
        print(getTxt(l.read()))
        l.close()


def Welcome():
    with open('./plugin/logos/welcomeafterlogin.txt', 'r', encoding='utf8') as l:
        print(getTxt(l.read()))
        l.close()


def choice():
    with open('./plugin/logos/choice.txt', 'r', encoding='utf8') as l:
        print(getTxt(l.read(),
                     "Tips:選擇登入或註冊"
                     ))
        l.close()


def postlist():
    with open('./plugin/logos/postlist.txt', 'r', encoding='utf8') as l:
        print(getTxt(l.read(),
                     "Tips:？？？"
                     ))
        l.close()


def gifText():
    while True:
        for i in range(1, 62):
            with open('./logos/emo/{}.txt'.format(i), 'r', encoding='utf8') as l:
                print(l.read())
                clear()


def test():
    with open('./plugin/logos/test.txt', 'r', encoding='utf8') as l:
        print(getTxt(l.read(),
                     "Tips:選擇登入或註冊"
                     ))
        l.close()


if __name__ == "__main__":
    gifText()
