from plugin import clientServer, logo
from datetime import datetime
# 列出文章列表
# 新增文章


class articleAction():
    def __init__(self, userData):
        self.userData = userData
        self.action = clientServer.client()

    def alert(self, msg):
        print("＊{}＊".format(msg))

    def listPosts(self):
        def posts(data):
            hr = "－－－－－－－－－－－－－－－－－－－－－－－－"
            for i, post in enumerate(data):
                postStr = "[{}]\n[文章標題]{}\n[發表內容(10字預覽)]{}\n[發布時間]{}\n{}".format(
                    i+1, post[0], post[1], str(datetime.date(post[3])) + ' ' + str(datetime.time(post[3])), hr)
                print(postStr)
        logo.postlist()
        result = self.action.connect(2, {'act': 'postlist'})[0]
        posts(result)
    
    def postForm(self):
        pass


if __name__ == "__main__":
    test = articleAction({})
    test.listPosts()
