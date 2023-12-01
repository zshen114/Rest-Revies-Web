from rest_framework import serializers
from api.models import Restaurant


class RestaurantsSerializer(serializers.ModelSerializer):

    ratings_avg = serializers.SerializerMethodField()

    class Meta:
        model = Restaurant
        fields = ['id', 'restaurant_owner', 'name', 'category', 'country', 'street', 'city',
                  'zip', 'website', 'phone', 'opening_hours', 'price_level', 'restaurant_pic', 'ratings_avg']
        read_only_fields = ['id']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        return {
            **data,
            'ratings_count': instance.restaurants.count(),
        }

    @staticmethod
    def get_ratings_avg(instance):
        try:
            return sum([comment.rating for comment in instance.restaurants.all()])/instance.restaurants.count()
        except ZeroDivisionError:
            return 0


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Restaurant
        fields = ['category']
