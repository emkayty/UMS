from django.urls import path
from .api import router
urlpatterns = [path('', router.urls)]
