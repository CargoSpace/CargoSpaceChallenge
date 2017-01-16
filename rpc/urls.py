from django.conf.urls import url

from modernrpc.views import RPCEntryPoint

urlpatterns = [
    # ... other views

    url(r'^rpc/', RPCEntryPoint.as_view()),
]