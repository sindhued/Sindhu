"""
URL configuration for sindhu_blog project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from .views import CommentHistoryForAuthorView,MyCommentHistoryView,Recent5LikedBlogView,Top5CommentedBlogView,Top5LikedandDislikedBlogView,BlogListView , BlogDetailView, LoginView, RegisterView, LogoutView, LikeView, DislikeView, CommentView, UserBlogDetailView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/',BlogListView.as_view(), name='home'),
    path('blogdetail/<int:pk>/', BlogDetailView.as_view(), name='blogdetail'),
    path('login/',LoginView.as_view(), name='login'),
    path('register/',RegisterView.as_view(), name='register'),
    path('logout/',LogoutView.as_view(),name='logout'),
    path('like/<int:pk>/', LikeView, name='like'),
    path('dislike/<int:pk>/', DislikeView, name='dislike'),
    path('comment/<int:pk>/',CommentView,name='comment'),
    path('userblog/', UserBlogDetailView,name='userblog'),
    path('topcommentedblogs/', Top5CommentedBlogView, name='topcommentedblogs'),
    path('toplikedanddislikedblogs/', Top5LikedandDislikedBlogView, name='toplikedanddislikedblogs'),
    path('recent5likedblogs/', Recent5LikedBlogView, name='recent5likedblogs'),
    path('mycommenthistory/<int:pk>', MyCommentHistoryView, name='mycommenthistory'),
    path('commenthistoryforauthor/', CommentHistoryForAuthorView, name='commenthistoryforauthor'),

]