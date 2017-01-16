from channels.routing import route, include
# from app.consumers import ws_connect, ws_message, ws_disconnect
from app.consumers import ws_add, ws_message, ws_disconnect

#pre auth channels
# channel_routing = [
# 	route("http.request", "app.consumers.http_consumer"),
#
#     # route("websocket.connect", ws_connect),
#     # route("websocket.receive", ws_message),
#     # route("websocket.disconnect", ws_disconnect),
# ]
http_routing = [
	route("http.request", "app.consumers.http_consumer"),
]
chat_routing = [
	route("websocket.connect", ws_add,
		path=r"^/(?P<room>[a-zA-Z0-9_]+)/$"),
    route("websocket.disconnect", ws_disconnect),
]

routing = [
   	include(chat_routing, path=r"^/chat"),
    include(http_routing),
]
