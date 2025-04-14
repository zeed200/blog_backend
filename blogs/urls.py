from django.urls import path
from . import views

urlpatterns = [
    path('', views.PostList.as_view(), name='home'),
    # path('about/', views.about, name='about'),
    path('detail/<int:post_id>', views.PostDetail.as_view(), name='detail'),
    path('comment_post/<int:post_id>', views.CommentPost.as_view(), name='comment_post'),
    path('new_post/', views.CreatePost.as_view(), name='new_post'),
    path('detail/<int:post_id>/update/', views.UpdatePost.as_view(), name='post-update'),
    path('detail/<int:post_id>/delete/', views.PostDelete.as_view(), name='post-delete'),
]