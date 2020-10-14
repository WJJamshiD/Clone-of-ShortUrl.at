from django.urls import path
from .views import wildcard_redirect

urlpatterns = [
    path('<path>/',wildcard_redirect),
]

