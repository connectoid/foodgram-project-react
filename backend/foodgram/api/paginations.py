from rest_framework.pagination import PageNumberPagination


class RecipePageNumberPagination(PageNumberPagination):
    page_size_query_param = 'limit'
    page_size = 6


class ShoppingCartPageNumberPagination(PageNumberPagination):
    page_size_query_param = 'limit'
    page_size = 10
