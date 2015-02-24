from django.conf.urls import patterns, url, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from ChatApp import views

urlpatterns = patterns('',
    url(r'^index/', views.index, name='index'),
    url(r'^login/', views.login_user, name='login_user'),
    url(r'^logout/', views.logout_user, name='logout_user'),
    url(r'^signup/', views.signup, name='signup'),
    url(r'^profile/', views.profile, name='my_profile'),
    url(r'^chat/$', views.chat, name='chat'),
    url(r'^edit_profile/$', views.edit_profile, name='edit_profile'),
    url(r'^edit_account/$', views.edit_account, name='edit_account'),
    url(r'^upload_pic/$', views.upload_pic, name='upload_pic'),
    url(r'^profiles/(?P<username>\w{0,50})/$', views.profile, name='friend_profile'),
    url(r'^matches/', views.matches, name='matches'),
    url(r'^qb/', views.qb, name='qb'),
    url(r'^create_match/', views.create_match, name='create_match'),
    url(r'^reject_match/', views.reject_match, name='reject_match'),
    url(r'^accounts/', include('allauth.urls')),
)

urlpatterns += staticfiles_urlpatterns()
