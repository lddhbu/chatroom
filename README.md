chatroom
========
一个在线聊天室，考虑以下几点：
1. 使用OpenID登录，支持Google的OpenID。
2. 防止恶意灌水,目前只用了两个限制，一是内容长度，一是本次内容和上次的相似度（采用编辑距离算法）。需要改进。
3. 支持同时和多人聊天。
4. 使用sockjs调用Websocket，服务端sockjs-tornado。

