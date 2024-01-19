from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('like/<int:post_id>/', views.like_post, name='like_post'),
    path('comment/<int:post_id>/', views.comment_post, name='comment_post'),  # Add this line
    # Add other URLs as needed
]
