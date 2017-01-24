from . import consumers
from channels.routing import route

channel_routing = {
    # route('websocket.connect', 'websucks.consumers.ws_connect',
    #       path=r'^/socket/(?P<user_id>[^/]+)/$/(?P<contest_id>[^/]+)/$'),
    # route('websocket.receive', 'websucks.consumers.ws_receive'),
    # route('websocket.receive', 'websucks.consumers.ws_disconnect'),
    
    'websocket.connect': consumers.ws_connect,
    'websocket.receive': consumers.ws_receive,
    'websocket.disconnect': consumers.ws_disconnect,
}
