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



