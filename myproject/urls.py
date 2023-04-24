"""myproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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

urlpatterns = [
    
]
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from myapp.views import (
    RegisteredUserView,
    UserLoginView,
    BlogCreateView,
    BlogList,
    CommentCreateView

)

urlpatterns = [
    path("admin/", admin.site.urls),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/register/', RegisteredUserView.as_view(), name='register'),
    path('api/login/', UserLoginView.as_view(), name='user-login'),
    path('api/blogpost/', BlogCreateView.as_view(), name='blogpost'),
    path('api/comment/<int:blog_id>', CommentCreateView.as_view(), name='comment'),
    path('blogs/', BlogList.as_view(), name='blog-list'),
    # path('api/blogposts/<int:pk>/', BlogPostDetail.as_view(), name='blogpost_detail'),
    # path('api/comments/', CommentList.as_view(), name='comment_list'),
]
