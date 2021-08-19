from django.urls import path
from social.views import (PostListView, PostDetailView,
                          PostEditView, PostDeleteView,
                          CommentDeleteView, ProfileView,
                          CommentEditView, ProfileEditView,)


urlpatterns = [
    path('',PostListView.as_view(),name='post_list'),
    path('post/<int:pk>/',PostDetailView.as_view(),name='post_detail'),
    path('post/edit/<int:pk>/',PostEditView.as_view(),name='post_edit'),
    path('post/delete/<int:pk>/',PostDeleteView.as_view(),name='post_delete'),
    path('edit_comment/<int:pk>/',CommentEditView.as_view(),name='comment_edit'),
    path('post/<int:post_pk>/comment/delete/<int:pk>',CommentDeleteView.as_view(),name='comment_delete'),
    path('profile/<int:pk>/', ProfileView.as_view(),name='profile'),
    path('profile/<int:pk>/edit',ProfileEditView.as_view(),name='profile_edit')
 ]
