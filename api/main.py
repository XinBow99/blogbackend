from flask import Flask, request
from flask_restful import reqparse, abort, Api, Resource

import clientServer
import hashString
import logicClient
import Gmail

app = Flask(__name__)
api = Api(app)

wrongProtocol = {
    'status': 0,
    'msg': 'wrongProtocol!'
}


class register(Resource):

    def get(self):
        thisP = wrongProtocol
        thisP.update({'path': '[GET]register'})
        return thisP

    def post(self):
        try:
            c = clientServer.client()
            arg = dict(request.get_json(force=False))
            data = {
                'act': 'register',
                'name': arg['name'],
                'nickname': arg['nickname'],
                'account': arg['account'],
                'password': arg['password'],
                'school': arg['school'],
                'email': arg['email']
            }
            print(data)
            r = logicClient.logic(c.connect(0, data))
            return r
        except:
            return wrongProtocol


class login(Resource):

    def get(self):
        thisP = wrongProtocol
        thisP.update({'path': '[GET]login'})
        return thisP

    def post(self):
        try:
            c = clientServer.client()
            arg = dict(request.get_json(force=False))
            data = {
                'act':  'login',
                'account': arg['account'],
                'password': arg['password']
            }
            print(data)
            r = logicClient.logic(c.connect(1, data))
            return r
        except:
            return wrongProtocol


class article(Resource):
    def __init__(self):
        self.c = clientServer.client()

    def get(self):
        data = {
            'act': 'postlist'
        }
        try:
            args = request.args
            if 'pid' in args:
                data.update(
                    {'post_ID': args['pid']}
                )
        except:
            pass
        print(data)
        return logicClient.logic(self.c.connect(2, data))

    def post(self):
        try:
            arg = dict(request.get_json(force=False))
            data = {
                'act': 'post',
                'title': arg['title'],
                'content': arg['content'],
                'class_ID': arg['class_ID'],
                'token': arg['token']
            }
            print(data)
            r = logicClient.logic(self.c.connect(3, data))
            return r
        except:
            return wrongProtocol

    def delete(self):
        data = {
            'act': 'postDel',
        }
        try:
            args = request.args
            if 'pid' in args:
                data.update(
                    {'post_ID': args['pid']}
                )
            arg = dict(request.get_json(force=False))
            data.update(
                {'token': arg['token']}
            )
        except:
            pass
        print(data)
        return logicClient.logic(self.c.connect(4, data))

    def put(self):
        data = {
            'act': 'postEdit',
        }
        try:
            arg = dict(request.get_json(force=False))
            args = request.args
            data.update({
                'post_ID': args['pid'],
                'title': arg['title'],
                'content': arg['content'],
                'token': arg['token']
            })
            print(data)
            r = logicClient.logic(self.c.connect(5, data))
            return r
        except:
            return wrongProtocol


class comment(Resource):
    def __init__(self):
        self.c = clientServer.client()

    def post(self):
        try:
            arg = dict(request.get_json(force=False))
            args = request.args
            data = {
                'act': 'comment',
                'post_ID': args['pid'],
                'msg_content': arg['content'],
                'token': arg['token']
            }
            print(data)
            r = logicClient.logic(self.c.connect(6, data))
            return r
        except:
            return wrongProtocol

    def delete(self):
        data = {
            'act': 'commentDel',
        }
        try:
            args = request.args
            if 'pid' in args and 'mid' in args:
                data.update(
                    {
                        'post_ID': args['pid'],
                        'msg_ID': args['mid']
                    }
                )
            arg = dict(request.get_json(force=False))
            data.update(
                {'token': arg['token']}
            )
        except:
            pass
        print(data)
        return logicClient.logic(self.c.connect(8, data))

    def put(self):
        data = {
            'act': 'commentEdit',
        }
        try:
            arg = dict(request.get_json(force=False))
            args = request.args
            data.update({
                'post_ID': args['pid'],
                'msg_ID': args['mid'],
                'msg_content': arg['content'],
                'token': arg['token']
            })
            print(data)
            r = logicClient.logic(self.c.connect(7, data))
            return r
        except:
            return wrongProtocol


class likes(Resource):
    def get(self):
        data = {}
        try:
            c = clientServer.client()
            arg = dict(request.get_json(force=False))
            if 'pid' in arg:
                data = {
                    'act': 'Like',
                    'from': arg['from'],
                    'post_ID': arg['pid'],
                    'token': arg['token']
                }
            elif 'mid' in arg:
                data = {
                    'act': 'Like',
                    'from': arg['from'],
                    'msg_ID': arg['mid'],
                    'token': arg['token']
                }
            print(data)
            r = logicClient.logic(c.connect(9, data))
            return r
        except:
            return wrongProtocol


api.add_resource(register, '/register')
api.add_resource(login, '/login')
api.add_resource(article, '/article')
api.add_resource(comment, '/comment')
api.add_resource(likes, '/likes')
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8763, debug=False)
