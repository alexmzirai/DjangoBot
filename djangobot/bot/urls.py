from django.conf.urls import url, include
from .views import BOT_TOKEN


urlpatterns = [
	url(r'^BOT_TOKEN/', name='bot' ),
]