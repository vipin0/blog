from django.conf.urls import url

from . import views
from django.urls import path
from django.conf.urls.static import static

urlpatterns = [
    path('', views.PostList.as_view(), name='home'),
    # path('<slug:slug>/', views.PostDetail.as_view(), name='post_detail'),
    path('<slug:slug>/', views.post_detail, name='post_detail'),
    # url(r'^(?P<pk>)/new/$', views.new_post, name='new_post'),
    path('new_post/', views.new_post, name='new_post'),
]
