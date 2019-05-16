from django.conf.urls import url
from summarizer import views


urlpatterns = [
    url('signup/', views.signup,name='signup'),
    url(r'^sumrz/$', views.sumrz, name='sumrz'),
    url(r'^wrd/$', views.wrd, name='wrd'),
    
]

