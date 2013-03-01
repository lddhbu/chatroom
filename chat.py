# encoding: utf-8
try:
    import simplejson as json
except ImportError:
    import json  # Python 2.6+
import time
import sockjs.tornado
import tornado.web
from base import BaseHandler
import tornado.escape

_SPAM_LEN_LIMIT=5
_SPAM_SIM_LIMIT=2.0

def similar_degrees(s1,s2):
    """
    检查两个字符串的相似度，抽象为编辑距离问题，基于动态规划思想，时间复杂度为O(mn)，空间复杂度为O(n)。
    相似度和“编辑距离”成反相关，和字符串的长度成正相关，这里我简单的认为相似度=“长度”/“编辑距离“(这里的长度为m和n较长者)。
    d[0]表示上次最优结果，d[1]表示这次最优结果
    """
    m=len(s1)
    n=len(s2)
    d=[[i for i in range(n+1)] for j in [0,1]]
    for i in range(1,m+1):
        d[0][0]=i-1#边界条件，上一次
        d[1][0]=i#边界条件，本次
        for j in range(1,n+1):
            cost=(s1[i-1]!=s2[j-1] and 1 or 0)+d[0][j-1]#替换
            temp=cost>d[1][j-1]+1 and d[1][j-1]+1 or cost#插入
            d[1][j]=temp>d[0][j]+1 and d[0][j]+1 or temp#插入
        for j in range(1,n+1):
            d[0][j]=d[1][j]

    length=d[1][n]#编辑距离
    ret=max(m,n)/(length+1.0)
    return ret


class ChatRoomHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.render("chatroom.html",messages=MessageMixin.catchs,clients=MessageMixin.clients)

class MessageMixin(object):
    clients=set()
    catchs=[]

    def add_client(cls,client):
        cls.clients.add(client)
        now=time.strftime('%Y-%m-%d %H:%M:%S')
        cls.catchs.append([client.name,'has joined',now])
        for client in cls.clients:
            client.send(tornado.escape.json_encode({'type':1,'id':id(client),'time':now,'user':client.name,'message':'has joined'}))


    def remove_client(cls,client):
        cls.clients.remove(client)
        now=time.strftime('%Y-%m-%d %H:%M:%S')
        cls.catchs.append([client.name,'has left',now])
        for client in cls.clients:
            client.send(json.dumps({'type':2,'id':id(client),'time':now,'user':client.name,'message':'has left'}))

    def new_message(cls,name,message):
        now=time.strftime('%Y-%m-%d %H:%M:%S')
        cls.catchs.append([name,message,now])
        for client in cls.clients:
            client.send(json.dumps({'type':3,'time':now,'user':name,'message':message}))

    def is_spam(self):
        """
        有两个限制，一是字符串长度，二是和上一次的发言的相似度
        """


class SocketHandler(sockjs.tornado.SockJSConnection,MessageMixin):
    """

    """
    def on_open(self,info):
        """
        """
        print "open one"
        user=tornado.escape.json_decode(self.session.handler.get_secure_cookie("user"))
        if not user:
            self.close()
        else:
            self.name=user['name']
            self.add_client(self)


    def on_close(self):
        """
        """
        self.remove_client(self)

    def on_message(self,message):
        self.new_message(self.name,message)



