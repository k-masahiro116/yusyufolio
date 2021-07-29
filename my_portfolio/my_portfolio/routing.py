import sys
sys.path.append("/Users/masahiro/Desktop/my_portfolio/my_portfolio/")
sys.path.append("../")
from chat import routing
from chat.consumers import Chatconsumer

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application


channel_routing = {}