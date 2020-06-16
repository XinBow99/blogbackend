import clientServer
import hashString
from datetime import date, datetime


def rowPost(data):
    rl = []
    for d in data:
        cla = ""
        if str(d[0]) == 'None':
            cla = "其他"
        else:
            cla = str(d[0])
        if str(d[7]) == "0":
            returnDic = {}
            returnDic['postClass'] = "null"
            returnDic['postId'] = "null"
            returnDic['postTitle'] = "null"
            returnDic['postViews'] = "null"
            returnDic['postContent'] = "null"
            returnDic['postTime'] = "null"
            returnDic['postLikes'] = "null"
            returnDic['postNick'] = "null"
            returnDic['postAccount'] = "null"
            returnDic['postSchool'] = "null"
            rl.append(returnDic)
        elif str(d[7]) == "1":
            returnDic = {}
            returnDic['postClass'] = cla
            returnDic['postId'] = d[1]
            returnDic['postTitle'] = d[2]
            returnDic['postContent'] = d[3]
            returnDic['postViews'] = d[4]
            returnDic['postTime'] = d[5].strftime('%Y-%m-%d %H:%M:%S')
            returnDic['postLikes'] = d[6]
            returnDic['postNick'] = d[8]
            returnDic['postAccount'] = d[9]
            returnDic['postSchool'] = d[10]
            rl.append(returnDic)
    yield rl


def rowComments(data):
    rl = []
    for d in data:
        returnDic = {}
        returnDic['msgId'] = d[0]
        returnDic['msgContent'] = d[3]
        returnDic['msgLikes'] = d[5]
        returnDic['msgTime'] = d[4].strftime('%Y-%m-%d %H:%M:%S')
        returnDic['msgNick'] = d[9]
        returnDic['msgSchool'] = d[12]
        rl.append(returnDic)
    yield rl


def logic(data):
    if data == "LoginError":
        return {
            'status': 0,
            'msg': '登入驗證失敗！'
        }
    result, command = data
    if command == 0:
        resDict = {
            'status': 1,
            'msg': ''
        }
        if result == None:
            resDict['status'] = 0
            resDict['msg'] = "註冊失敗！可能是帳號重複！或是欄位尚未填寫！"
        elif str(result) == '1':
            resDict['status'] = 1
            resDict['msg'] = "註冊成功！快去登入看看吧！"
        return resDict
    elif command == 1:
        resDict = {
            'status': 1,
            'msg': '登入成功！！！'
        }
        if result == None:
            resDict['status'] = 0
            resDict['msg'] = '登入失敗！你可能記錯帳號了'
        else:
            resDict['token'] = hashString.encode(result[0])
        return resDict
    elif command == 2:
        resDict = {
            'status': 1,
        }
        if result[1] == 'allPost':
            post = next(rowPost(result[0]))
            resDict['post'] = post
        else:
            singlePost = result[0]
            commentList = result[1]

            if len(singlePost) != 1:
                resDict['status'] = 0
                resDict['msg'] = '沒有此篇貼文！'
            elif len(singlePost) == 1:
                post = next(rowPost(singlePost))[0]
                post['postComments'] = next(rowComments(commentList))
                resDict['post'] = post
        return resDict
    elif command == 3:
        resDict = {
            'status': 1,
            'msg': '發布貼文成功！'
        }
        if result == None or result == 0:
            resDict = {
                'status': 0,
                'msg': '發布失敗'
            }
        return resDict
    elif command == 4:
        resDict = {
            'status': 1,
            'msg': '刪除貼文成功！'
        }
        if result == 0:
            resDict['status'] = 0
            resDict['msg'] = "刪除失敗:("
        return resDict
    elif command == 5:
        resDict = {
            'status': 1,
            'msg': '編輯成功！'
        }
        if result == 0:
            resDict['status'] = 0
            resDict['msg'] = "編輯失敗:("
        return resDict
    elif command == 6:
        resDict = {
            'status': 1,
            'msg': '發布留言成功！'
        }
        if result == 0:
            resDict['status'] = 0
            resDict['msg'] = "發布留言失敗:("
        return resDict
    elif command == 7:
        resDict = {
            'status': 1,
            'msg': '留言編輯成功！'
        }
        if result == 0:
            resDict['status'] = 0
            resDict['msg'] = '留言編輯失敗:('
        return resDict
    elif command == 8:
        resDict = {
            'status': 1,
            'msg': '留言刪除成功！'
        }
        if result == 0:
            resDict['status'] = 0
            resDict['msg'] = '留言刪除失敗:('
        return resDict
    elif command == 9:
        resDict = {
            'status': 1,
            'msg': '讚啦😎'
        }
        if result == '' or result == None:
            resDict['status'] = 0
            resDict['msg'] = "按讚失敗"
        return resDict


if __name__ == "__main__":
    test = clientServer.client(1)
    testData0 = {
        'act': 'register',
        'name': '',
        'nickname': '',
        'account': '',
        'password': '',
        'school': '',
        'email': 'test@gmail.com',
    }
    testData1 = {
        'act': 'login',
        'account': '',
        'password': ''
    }
    testData2 = {
        'act': 'postlist',
        'post_ID': 8
    }
    testData3 = {
        'act': 'post',
        'title': '高科發大財！',
        'content': '韓總一路好走',
        'class_ID': '1',
        'token': ''
    }
    testData4 = {
        'act': 'postDel',
        'post_ID': '1',
        'token': ''
    }
    testData5 = {
        'act': 'postEdit',
        'post_ID': '3',
        'token': '',
        'title': '修改',
        'content': '幹你娘'
    }
    testData6 = {
        'act': 'comment',
        'post_ID': '3',
        'msg_content': 'test2',
        'token': '',
    }
    testData7 = {
        'act': 'commentEdit',
        'token': '',
        'post_ID': '3',
        'msg_ID': '2',
        'msg_content': '嗨嗨1234567'
    }
    testData8 = {
        'act': 'commentDel',
        'token': '',
        'post_ID': '3',
        'msg_ID': '3',

    }
    testData9 = {
        'act': 'Like',
        'from': '2',
        'token': '',
        'msg_ID': '2',

    }
    print(logic(test.connect(9, testData9)))
