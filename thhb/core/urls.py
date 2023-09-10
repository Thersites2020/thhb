from django.urls import path

from . import views


app_name = 'core'
urlpatterns = [
    path('', views.home, name='home'),
    path('under_construction/', views.no_access_view, name='under_construction'),
    path('post_list', views.post_list, name='post_list'),
    path('create_post', views.create_blogpost, name='create_post'),
    path('userpage', views.userpage, name='user_page'),
    path('update_post/<slug:post_slug>/', views.update_blogpost, name='update_post'),
    path('<slug:post_slug>/', views.show_single_post, name='single_post'),
]
