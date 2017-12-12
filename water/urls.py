from django.conf.urls import url
from . import views

app_name = 'water'


urlpatterns = [
    url(r'^$', views.index, name='index'),#for index (home)page
    url(r'^(?P<brand_id>[0-9]+)/$', views.detail, name='detail'),#detail of each id
    url(r'^login/$', views.login_view, name='login'),#for login
    url(r'^signup/$',views.Register_View, name='signup'),#for signup
    url(r'^profile/$', views.user_profile, name='profile'),
    url(r'^waterworld/$', views.logoutView, name='logout'),
    url(r'^Pincode/$', views.Pincode, name='Pincode'),
    #url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),

]