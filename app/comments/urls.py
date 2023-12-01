from django.urls import path
from .views import (CommentListCreateAPIView,
                    CommentGetDeleteUpdateView,
                    GetAllCommentsByUserIDView,
                    LikeUnlikeCommentView,
                    CommentReactionsListAPIView,
                    SearchComment)

urlpatterns = [
    path('', CommentListCreateAPIView.as_view(), name='restaurant-comment'),
    path('<int:pk>/', CommentGetDeleteUpdateView.as_view(), name='comment-get-update-delete'),
    path('user/<int:user_id>/', GetAllCommentsByUserIDView.as_view(), name='user-search'),
    path('reaction/<comment_id>', LikeUnlikeCommentView.as_view(), name='like-unlike-comment'),
    path('reactions', CommentReactionsListAPIView.as_view(), name='all-comments-reactions'),

    # Search example: /api/comments/search/?search=<keyword in body>
    path('search/', SearchComment.as_view(), name='comment-search'),

]
