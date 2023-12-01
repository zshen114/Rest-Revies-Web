from rest_framework import serializers
from restaurants.serializers import RestaurantsSerializer
from api.models import (Comment,
                        Reaction)


class CommentsSerializer(serializers.ModelSerializer):

    # restaurant = RestaurantsSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'author', 'restaurant', 'body', 'image', 'rating', 'created', 'modified']
        read_only_fields = ['id', 'created', 'modified']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        return {
            **data,
            'likes_counter': instance.comments.count(),
        }


class ReactionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Reaction
        fields = ['id', 'user_reacted', 'comment']
        read_only_fields = ['id']