from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework import filters

from api.models import (Comment,
                        Reaction)
from .serializers import (CommentsSerializer,
                          ReactionSerializer)
from rest_framework.generics import get_object_or_404
from django.db.models import Q


class CommentListCreateAPIView(generics.ListCreateAPIView):
    """
    Class to GET all Comments or POST a Comment for a restaurant
    """
    serializer_class = CommentsSerializer
    queryset = Comment.objects.all()

    def post(self, request):
        serializer = CommentsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"Status 201": "Comment created succesfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentGetDeleteUpdateView(generics.RetrieveUpdateDestroyAPIView):
    """
    Class to GET - PUT/PATCH (UPDATE) - DELETE: Comment by id
    """
    serializer_class = CommentsSerializer

    def get_object(self, pk):
        comment = get_object_or_404(Comment, pk=pk)
        return comment

    def get(self, request, pk):
        comment = self.get_object(pk)
        serializer = CommentsSerializer(comment)
        return Response(serializer.data)

    def put(self, request, pk):
        comment = self.get_object(pk)
        serializer = CommentsSerializer(comment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"Status 201": "Comment updated succesfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        comment = self.get_object(pk)
        comment.delete()
        return Response({"Status 204": "Comment deleted succesfully"}, status=status.HTTP_204_NO_CONTENT)


class GetAllCommentsByUserIDView(generics.ListAPIView):
    """
    Class to GET all the Comments by a specific User in chronological order
    """
    serializer_class = CommentsSerializer

    def get_queryset(self, *args, **kwargs):
        kwargs = self.kwargs  # --> a dictionary with the url's parameter {'author_id': '2'}
        kw_id = kwargs.get('user_id')  # --> returns the value of key='author_id'
        return Comment.objects.filter(author=kw_id)


class CommentReactionsListAPIView(generics.ListAPIView):
    """
    Class to GET all Reactions on Comments
    """
    serializer_class = ReactionSerializer
    queryset = Reaction.objects.all()


class LikeUnlikeCommentView(generics.ListCreateAPIView):
    """
    Class to Like or Remove a Like from a comment
    """
    serializer_class = ReactionSerializer

    def get_object(self, comment_id):
        comment = get_object_or_404(Comment, pk=comment_id)
        return comment

    def get(self, request, comment_id):
        comment = self.get_object(comment_id)
        serializer = CommentsSerializer(comment)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        comment_id = self.kwargs.get('comment_id')
        comment = Comment.objects.get(id=comment_id)
        Reaction.objects.get_or_create(user_reacted=self.request.user, comment=comment)
        return Response({"Status 201": "Comment liked succesfully"}, status=status.HTTP_201_CREATED)

    def delete(self, request, comment_id):
        comment_id = self.kwargs.get('comment_id')
        comment = Comment.objects.get(id=comment_id)
        Reaction.objects.filter(Q(user_reacted=self.request.user)
                                & Q(comment=comment)).delete()
        return Response({"Status 204": "Comment unliked succesfully"}, status=status.HTTP_204_NO_CONTENT)


class SearchComment(generics.ListAPIView):
    """
    Class to Search Comments
    """

    serializer_class = CommentsSerializer
    queryset = Comment.objects.all()
    filter_backends = (filters.SearchFilter,)
    search_fields = ('body',)
