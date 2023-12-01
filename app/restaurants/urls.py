from django.urls import path
from .views import (GetAllRestaurantsView,
                    GetPostUpdateDeleteRestaurantView,
                    GetRestaurantByCategoryView,
                    GetRestaurantByUserIDView,
                    CategoriesView,
                    SearchRestaurant)

urlpatterns = [
    path("", GetAllRestaurantsView.as_view(), name="get-list-of-all-restaurants"),
    path("category/<str:category>/", GetRestaurantByCategoryView.as_view(), name="get-restaurant-by-category"),
    path("<int:pk>/", GetPostUpdateDeleteRestaurantView.as_view(), name="get-post-delete-update-restaurant"),
    path("user/<int:user_id>/", GetRestaurantByUserIDView.as_view(), name="get-restaurants-by-user-id"),
    path("categories/", CategoriesView.as_view(), name="get-restaurants-categories"),

    # Search example: /api/restaurants/?search=<name or category or city or country>
    path('search/', SearchRestaurant.as_view(), name='restaurant-search'),

]



