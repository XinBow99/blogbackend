import mysql.connector
from mysql.connector import Error
from mysql.connector import errorcode
import hashlib
import hashString
import json
import Gmail


class client():
    def __init__(self, debug=0):
        self.host = "localhost"
        self.port = ""
        self.database = ""
        self.user = ""
        self.password = ""
        self.MariaDB = ""
        self.debug = debug

    def alert(self, msg):
        if self.debug == 1:
            print(msg)

    def connect(self, action="nothing", datas={
        'act': 'i dont know'
    }):
        result = ""
        try:
            MariaDB = mysql.connector.connect(
                host=self.host,
                port=self.port,
                database=self.database,
                user=self.user,
                password=self.password
            )
            if MariaDB.is_connected():
                db_Info = MariaDB.get_server_info()
                self.alert(
                    "Connected to MySQL Server version {}".format(db_Info))
                cursor = MariaDB.cursor()
                cursor.execute("select database();")
                record = cursor.fetchone()
                self.alert("You're connected to database: {}".format(record))
                self.MariaDB = MariaDB, cursor
                if action != "nothing" and action != "hashTest":
                    result = self.actionDB(action, datas)
                elif action == "hashTest":
                    self.alert('HS')
                    self.forHashDateSheet('post', datas[0], datas[1])
                else:
                    pass
        except Error as e:
            self.alert("Error while connecting to MySQL{}".format(e))
        finally:
            if (MariaDB.is_connected()):
                cursor.close()
                self.MariaDB[1].close()
                MariaDB.close()
                self.MariaDB[0].close()
                self.alert("MySQL MariaDB is closed")
        return result

    def forHashDateSheet(self, method, key, md5):
        if method == "post":
            insertQuery = "INSERT INTO `bone_blog`.`keybase` (`key`, `md5`) VALUES ('{}', '{}');".format(
                key, md5)
            self.MariaDB[1].execute(insertQuery)
            self.MariaDB[0].commit()
            result = self.MariaDB[1].rowcount
            self.alert(result)

    def actionDB(self, commandId, datas):
        cmd = [
            'register',     # 0
            'login',        # 1
            'postlist',     # 2
            'post',         # 3
            'postDel',      # 4
            'postEdit',     # 5
            'comment',      # 6
            'commentEdit',  # 7
            'commentDel',   # 8
            'Like',         # 9
            'unlike'        # ------
        ]
        query = ""
        result = ""
        self.alert('test!')
        self.alert(commandId)
        self.alert(datas)
        self.alert(cmd[commandId])
        self.alert('----test----')
        # 登入驗證
        userId = ""

        def loginCheck(datas):
            if 'token' in datas:
                self.alert(datas)
                datas['token'] = hashString.decode(datas['token'])
                self.alert(datas)
                select_query = "SELECT User_ID FROM bone_blog.bone_member WHERE md5Hash = '{}'".format(
                    datas['token']
                )
                self.alert(select_query)
                self.MariaDB[1].execute(select_query)
                self.alert('loginCheck')
                result = self.MariaDB[1].fetchone()
                self.alert(result)
                if result == None:
                    self.alert('登入驗證失敗')
                    return False
                else:
                    userId = result[0]
                    self.alert('get userId is:{}'.format(userId))
                    return userId
            else:
                self.alert('登入驗證失敗')
                return False

        def skipCheck(commandId, datas):
            skipLoginPassRules = {
                'commandId': [0, 1, 2],
                'act': [cmd[0], cmd[1], cmd[2]]
            }
            if commandId in skipLoginPassRules['commandId'] and 'act' in datas and datas['act'] in skipLoginPassRules['act']:
                return True
            else:
                return False
        # 判斷操作是否需要登入驗證
        if skipCheck(commandId, datas):  # 不需要驗證登入
            self.alert('不需驗證登入')
            pass
        else:  # 需要驗證登入
            self.alert('進行登入驗證')
            userId = loginCheck(datas)
            if not userId:
                return 'LoginError'
            self.alert('登入驗證成功')
        ##########
        # register  id = 0 done!
        ##########
        if commandId == 0 and "act" in datas and datas['act'] == cmd[commandId]:
            def userRegister(datas):
                checkQuery = """SELECT * FROM bone_member WHERE `nickname`='{}' OR `account` = '{}' OR email = '{}'""".format(
                    datas['nickname'], datas['account'], datas['email'])
                self.MariaDB[1].execute(checkQuery)
                self.alert('Register Check')
                checkResult = self.MariaDB[1].fetchone()
                self.alert(checkResult)
                if checkResult != None:
                    return None
                m = hashlib.md5()
                m.update(datas['password'].encode("utf-8"))
                datas['password'] = m.hexdigest()

                m.update(json.dumps(datas).encode("utf-8"))

                insert_query = "INSERT INTO `bone_blog`.`bone_member` (`name`, `nickname`, `account`, `password`, `school`, `email`, `md5Hash`) VALUES ('{}', '{}', '{}', '{}', '{}', '{}','{}') ".format(
                    datas['name'], datas['nickname'], datas['account'], datas['password'], datas['school'], datas['email'], m.hexdigest())
                return insert_query
            query = userRegister(datas)
            if query != None:
                self.MariaDB[1].execute(query)
                self.MariaDB[0].commit()
                self.alert("{} Record inserted successfully about {} table".format(
                    self.MariaDB[1].rowcount, self.database))
                g = Gmail.Ginit()
                g.sendMsg('恭喜您加入骨頭部落格', '{}({})快去登入看看吧'.format(
                    datas['name'], datas['nickname']), datas['email'])
                result = self.MariaDB[1].rowcount
            else:
                result = None
        ##########
        # login     id = 1 done!
        ##########
        elif commandId == 1 and "act" in datas and datas['act'] == cmd[commandId]:
            def userLogin(datas):
                m = hashlib.md5()
                m.update(datas['password'].encode("utf-8"))
                datas['password'] = m.hexdigest()
                select_query = "SELECT `md5Hash` FROM bone_blog.bone_member WHERE ACCOUNT = '{}' AND PASSWORD = '{}'".format(
                    datas['account'],
                    datas['password']
                )
                return select_query

            self.alert('login')
            query = userLogin(datas)
            self.alert(query)
            self.MariaDB[1].execute(query)
            self.alert('login1')
            result = self.MariaDB[1].fetchone()
            self.alert(result)
        ##########
        # postList  id = 2 done!
        ##########
        elif commandId == 2 and "act" in datas and datas['act'] == cmd[commandId]:
            def listPosts(post_ID):
                select_query = ""
                if 'post_ID' in post_ID:
                    singlePostQuery = '''  SELECT 
                                            bone_class.class_name,
                                            bone_post.post_ID,
                                            bone_post.title,
                                            bone_post.content,
                                            bone_post.views,
                                            bone_post.post_time,
                                            bone_post.likes,
                                            bone_post.`enable`,
                                            bone_member.nickname,
                                            bone_member.account,
                                            bone_member.school
                                        FROM bone_post 
                                            JOIN bone_member 
                                            ON bone_post.User_ID = bone_member.User_ID
                                            LEFT JOIN bone_class 
                                            ON (bone_post.class_ID = bone_class.class_ID) 
                                            WHERE bone_post.post_ID = {}
                                    '''.format(post_ID['post_ID'])
                    commentQuery = """  SELECT *
                                    FROM bone_post_message
                                    LEFT JOIN bone_member 
                                    ON bone_post_message.User_ID=bone_member.User_ID
                                    WHERE bone_post_message.post_ID = {}
                                    """.format(post_ID['post_ID'])
                    select_query = (singlePostQuery, commentQuery)
                else:
                    select_query = '''
                    SELECT 
                                            bone_class.class_name,
                                            bone_post.post_ID,
                                            bone_post.title,
                                            bone_post.content,
                                            bone_post.views,
                                            bone_post.post_time,
                                            bone_post.likes,
                                            bone_post.`enable`,
                                            bone_member.nickname,
                                            bone_member.account,
                                            bone_member.school
                                        FROM bone_post 
                                            JOIN bone_member 
                                            ON bone_post.User_ID = bone_member.User_ID
                                            LEFT JOIN bone_class 
                                            ON (bone_post.class_ID = bone_class.class_ID) 
                    '''
                return select_query
            self.alert('Get Posts')
            query = listPosts(datas)
            if 'post_ID' in datas:
                self.alert(query[0])
                self.MariaDB[1].execute(query[0])
                multipleResult1 = self.MariaDB[1].fetchall()
                self.alert(query[1])
                self.MariaDB[1].execute(query[1])
                multipleResult2 = self.MariaDB[1].fetchall()
                result = (multipleResult1, multipleResult2)
            else:
                self.alert(query)
                self.MariaDB[1].execute(query)
                result = (self.MariaDB[1].fetchall(), 'allPost')
                self.alert(result)
        ##########
        # post      id = 3 done!
        ##########
        elif commandId == 3 and "act" in datas and datas['act'] == cmd[commandId]:
            def post(datas):
                if 'title' in datas and 'content' in datas:
                    if 'class_ID' in datas:
                        select_query = "INSERT INTO `bone_blog`.`bone_post` (`class_ID`, `User_ID`, `title`, `content`) VALUES ('{}','{}', '{}', '{}');".format(
                            datas['class_ID'],
                            userId,
                            datas['title'],
                            datas['content']
                        )
                    else:
                        select_query = "INSERT INTO `bone_blog`.`bone_post` (`User_ID`, `title`, `content`) VALUES ('{}', '{}', '{}');".format(
                            userId,
                            datas['title'],
                            datas['content']
                        )
                else:
                    return None
                return select_query
            self.alert('POST!')
            query = post(datas)
            if query != None:
                self.alert('GET POST SQL')
                self.MariaDB[1].execute(query)
                self.MariaDB[0].commit()
                self.alert("{} Record inserted successfully about {} table".format(
                    self.MariaDB[1].rowcount, self.database))
                result = self.MariaDB[1].rowcount
        ##########
        # delete    id = 4 done!
        ##########
        elif commandId == 4 and "act" in datas and datas['act'] == cmd[commandId]:
            def disenable(post_ID):
                select_query = "UPDATE `bone_blog`.`bone_post` SET `enable`='0' WHERE  `post_ID`={} AND `User_ID`={};".format(
                    post_ID,
                    userId
                )
                return select_query
            query = disenable(datas['post_ID'])
            self.MariaDB[1].execute(query)
            self.MariaDB[0].commit()
            result = self.MariaDB[1].rowcount
            if result == 0:
                self.alert('操作更新失敗')
            else:
                self.alert('操作更新成功')
        ##########
        # EDIT      id = 5 #done!
        ##########
        elif commandId == 5 and "act" in datas and datas['act'] == cmd[commandId]:
            def edit(postData):
                select_query = ""
                if 'post_ID' in postData and 'title' in postData and 'content' in postData:
                    select_query = '''UPDATE `bone_blog`.`bone_post` SET `title`='{}',`content`='{}' WHERE  `post_ID`={} AND `User_ID`={};'''.format(
                        postData['title'], postData['content'], postData['post_ID'], userId)
                else:
                    self.alert('Wrong command value id:{}'.format(commandId))
                return select_query
            query = edit(datas)
            self.MariaDB[1].execute(query)
            self.MariaDB[0].commit()
            result = self.MariaDB[1].rowcount
            if result == 0:
                self.alert('操作更新失敗')
            else:
                self.alert('操作更新成功')
        ##########
        # COMMENT   id = 6 done!
        ##########
        elif commandId == 6 and "act" in datas and datas['act'] == cmd[commandId]:
            def comment(datas):
                select_query = ""
                if 'msg_content' in datas and 'post_ID' in datas:
                    checkQuery = 'SELECT post_ID FROM bone_post WHERE post_ID = {}'.format(
                        datas['post_ID'])
                    self.alert(checkQuery)
                    self.MariaDB[1].execute(checkQuery)
                    checkResult = self.MariaDB[1].fetchone()
                    self.alert('check result:{}'.format(checkResult))
                    if checkResult == None:
                        return None
                    self.alert('Check Successful!')
                    select_query = "INSERT INTO `bone_blog`.`bone_post_message` (`post_ID`, `User_ID`, `msg_content`) VALUES ({}, {}, '{}');".format(
                        checkResult[0], userId, datas['msg_content']
                    )
                else:
                    self.alert('Wrong command value id:{}'.format(commandId))
                return select_query
            query = comment(datas)
            self.MariaDB[1].execute(query)
            self.MariaDB[0].commit()
            self.alert("{} Record inserted successfully about {} table".format(
                self.MariaDB[1].rowcount, self.database))
            result = self.MariaDB[1].rowcount
        ##########
        # comment Edit   id = 7 done!
        # comment del   id = 8 done
        ##########
        elif (commandId == 7 and "act" in datas and datas['act'] == cmd[commandId]) or (commandId == 8 and "act" in datas and datas['act'] == cmd[commandId]):
            def edit(datas):
                if 'msg_ID' in datas and 'post_ID' in datas:
                    checkQuery = 'SELECT post_ID FROM bone_post WHERE post_ID = {}'.format(
                        datas['post_ID'])
                    self.alert(checkQuery)
                    self.MariaDB[1].execute(checkQuery)
                    checkResult = self.MariaDB[1].fetchone()
                    self.alert('check result:{}'.format(checkResult))
                    if checkResult == None:
                        return None
                    post_ID = checkResult[0]
                    checkQuery = 'SELECT msg_ID FROM bone_post_message WHERE post_ID = {} AND msg_ID = {}'.format(
                        post_ID, datas['msg_ID'])
                    self.alert(checkQuery)
                    self.MariaDB[1].execute(checkQuery)
                    checkResult = self.MariaDB[1].fetchone()
                    self.alert('check result:{}'.format(checkResult))
                    if checkResult == None:
                        return None
                    msg_ID = checkResult[0]
                    checkQuery = 'SELECT `enable` FROM bone_post_message WHERE post_ID = {} AND msg_ID = {}'.format(
                        post_ID, msg_ID)
                    self.alert(checkQuery)
                    self.MariaDB[1].execute(checkQuery)
                    checkResult = self.MariaDB[1].fetchone()
                    self.alert('check result:{}'.format(checkResult))
                    if checkResult[0] == 0:
                        return None
                    if 'msg_content' in datas and commandId == 7:
                        editQuery = '''UPDATE `bone_blog`.`bone_post_message` SET `msg_content`='{}' WHERE  `msg_ID`={} AND `post_ID`={} AND `User_ID`={};'''.format(
                            datas['msg_content'], msg_ID, post_ID, userId)
                    elif not 'msg_content' in datas and commandId == 8:
                        editQuery = '''UPDATE `bone_blog`.`bone_post_message` SET `enable`={} WHERE  `msg_ID`={} AND `post_ID`={} AND `User_ID`={};'''.format(
                            0, msg_ID, post_ID, userId)
                    return editQuery
            query = edit(datas)
            if query != None:
                self.MariaDB[1].execute(query)
                self.MariaDB[0].commit()
                result = self.MariaDB[1].rowcount
            else:
                result = 0
            if result == 0 or result == None:
                self.alert('操作更新失敗')
            else:
                self.alert('操作更新成功')
        ##########
        # LIKE   id = 9 done!
        ##########
        elif commandId == 9 and "act" in datas and datas['act'] == cmd[commandId]:
            def like(datas):
                likeQuery = ""
                if 'from' in datas:
                    if int(datas['from']) > 0 and int(datas['from']) < 3:
                        self.alert('喜歡驗證成功')
                        if int(datas['from']) - 1 == 0 and 'post_ID' in datas:
                            checkQuery = 'SELECT enable FROM bone_post WHERE post_ID = {}'.format(
                                datas['post_ID'])
                            self.alert(checkQuery)
                            self.MariaDB[1].execute(checkQuery)
                            checkResult = self.MariaDB[1].fetchone()
                            self.alert('check result:{}'.format(checkResult))
                            if checkResult == None:
                                return None
                            enable = checkResult[0]
                            if int(enable) == 0:
                                return None
                            getLikesQuery = '''SELECT likes FROM bone_post WHERE post_ID = {}'''.format(
                                datas['post_ID'])
                            self.alert(getLikesQuery)
                            self.MariaDB[1].execute(getLikesQuery)
                            getLikesResult = self.MariaDB[1].fetchone()
                            self.alert(
                                'check result:{}'.format(getLikesResult))
                            if getLikesResult == None:
                                return None
                            likeQuery = '''UPDATE `bone_blog`.`bone_post` SET `likes`='{}' WHERE  `post_ID`={};'''.format(
                                int(getLikesResult[0]) + 1, datas['post_ID'])
                        elif int(datas['from']) - 1 == 1 and 'msg_ID' in datas:
                            checkQuery = 'SELECT enable FROM bone_post_message WHERE msg_ID = {}'.format(
                                datas['msg_ID'])
                            self.alert(checkQuery)
                            self.MariaDB[1].execute(checkQuery)
                            checkResult = self.MariaDB[1].fetchone()
                            self.alert('check result:{}'.format(checkResult))
                            if checkResult == None:
                                return None
                            enable = checkResult[0]
                            if int(enable) == 0:
                                return None
                            getLikesQuery = '''SELECT likes FROM bone_post_message WHERE msg_ID = {}'''.format(
                                datas['msg_ID'])
                            self.alert(getLikesQuery)
                            self.MariaDB[1].execute(getLikesQuery)
                            getLikesResult = self.MariaDB[1].fetchone()
                            self.alert(
                                'check result:{}'.format(getLikesResult))
                            if getLikesResult == None:
                                return None
                            likeQuery = '''UPDATE `bone_blog`.`bone_post_message` SET `likes`='{}' WHERE  `msg_ID`={};'''.format(
                                int(getLikesResult[0]) + 1, datas['msg_ID'])
                            if getLikesResult == None:
                                return None
                        else:
                            return None
                    else:
                        return None
                return likeQuery
            query = like(datas)
            if query != None:
                self.MariaDB[1].execute(query)
                self.MariaDB[0].commit()
                result = self.MariaDB[1].rowcount
            if result == 0 or query == None:
                self.alert('操作更新失敗')
            else:
                self.alert('操作更新成功')
        # self.alert(query)
        else:
            return None, commandId
        debugAlert = "{}\nQuery:{}\nRun Result:{}\nRun Id:{}\ncmd is:{}\ndatas Action is:{}\nuser id is:{}\n{}".format(
            '-----DEBUG ALERT-----',
            query,
            result,
            commandId,
            cmd[commandId],
            datas['act'],
            userId,
            '---DEBUG ALERT END---'
        )
        self.alert(debugAlert)
        return result, commandId


if __name__ == "__main__":
    test = client(1)
    
    test.connect(3, {})
