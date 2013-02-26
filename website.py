import tornado.ioloop
import tornado.web
import sockjs.tornado
import os,sys
from tornado.options import define,options

from auth import AuthLoginHandler,AuthLogoutHandler
from chat import SocketHandler
from base import IndexHandler
from chat import ChatRoomHandler

define("port",default=50081,help="run on the given port",type=int)

ChatRouter = sockjs.tornado.SockJSRouter(SocketHandler, '/socket')

class Application(tornado.web.Application):
	def __init__(self):
		handlers=[
			(r"/",IndexHandler),
            (r"/chatroom",ChatRoomHandler),
			(r"/auth/login",AuthLoginHandler),
			(r"/auth/logout",AuthLogoutHandler),
		]+ ChatRouter.urls
		settings=dict(
			cookie_secret="7pQHnYyvvPhDekB+KftG18InKZCrwIahp02DK",
			login_url="/auth/login",
			template_path=os.path.join(os.path.dirname(__file__),"templates"),
			static_path=os.path.join(os.path.dirname(__file__),"static"),
			xsrf_cookies=True,
			autoescape="xhtml_escape",
		)
		tornado.web.Application.__init__(self,handlers,**settings)

def main():
	tornado.options.parse_command_line()
	app=Application()
	argc=len(sys.argv)
	if argc<2:
		port=options.port
	else:
		port=int(sys.argv[1])
	print "listening on port: %s"%port
	app.listen(port)
	tornado.ioloop.IOLoop.instance().start()

if __name__=="__main__":
	main()
