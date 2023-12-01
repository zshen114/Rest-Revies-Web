from rest_framework import generics, status
from api.permissions import IsOwnerOrReadOnly
from rest_framework.response import Response
from rest_framework import filters

from restaurants.serializers import (RestaurantsSerializer,
                                     CategorySerializer)
from rest_framework.generics import (ListCreateAPIView,
                                     ListAPIView,
                                     RetrieveUpdateDestroyAPIView)

from rest_framework.generics import get_object_or_404
from api.models import Restaurant


class GetAllRestaurantsView(ListCreateAPIView):
    """
    Class to GET the list of all Restaurants or POST a new Restaurant
    """
    serializer_class = RestaurantsSerializer
    queryset = Restaurant.objects.all()
    permission_classes = [IsOwnerOrReadOnly]

    def post(self, request):
        serializer = RestaurantsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"Status 201": "Restaurant created succesfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetPostUpdateDeleteRestaurantView(RetrieveUpdateDestroyAPIView):
    """
    Class to GET - PUT - DELETE: Restaurant by id
    """
    serializer_class = RestaurantsSerializer

    def get_object(self, pk):
        restaurant = get_object_or_404(Restaurant, pk=pk)
        return restaurant

    def get(self, request, pk):
        restaurant = self.get_object(pk)
        serializer = RestaurantsSerializer(restaurant)
        return Response(serializer.data)

    def put(self, request, pk):
        restaurant = self.get_object(pk)
        serializer = RestaurantsSerializer(restaurant, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"Status 201": "Restaurant updated succesfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        restaurant = self.get_object(pk)
        restaurant.delete()
        return Response({"Status 204": "Restaurant deleted succesfully"}, status=status.HTTP_204_NO_CONTENT)


class GetRestaurantByCategoryView(ListAPIView):
    """
    Class to GET all the Restaurants by category
    """
    serializer_class = RestaurantsSerializer

    def get_queryset(self):
        category = self.kwargs.get("category").title()
        return Restaurant.objects.filter(category=category)


class GetRestaurantByUserIDView(generics.ListAPIView):
    """
    Class to Get the all the Restaurants by owner
    """
    serializer_class = RestaurantsSerializer

    def get_queryset(self, *args, **kwargs):
        kwargs = self.kwargs  # --> a dictionary with the url's parameter {'author_id': '2'}
        kw_id = kwargs.get('user_id')  # --> returns the value of key='author_id'
        return Restaurant.objects.filter(restaurant_owner=kw_id)


class CategoriesView(ListAPIView):
    """
    Class to GET the categories of the Restaurants
    """
    serializer_class = CategorySerializer
    queryset = Restaurant.objects.all()

    def get_queryset(self):
        categories = Restaurant.objects.values("category").distinct()

        return categories


class SearchRestaurant(generics.ListAPIView):
    """
    Class to Search Restaurants
    """

    serializer_class = RestaurantsSerializer
    queryset = Restaurant.objects.all()
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', 'category', 'city', 'country')
