from channels.routing import route
from app.consumers import ws_connect, ws_message, ws_disconnect

channel_routing = [
	route("http.request", "app.consumers.http_consumer"),
    route("websocket.connect", ws_connect),
    route("websocket.receive", ws_message),
    route("websocket.disconnect", ws_disconnect),
]
