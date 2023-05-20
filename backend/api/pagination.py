from rest_framework.pagination import PageNumberPagination

PAGE_SIZE: int = 6


class LimitPageNumberPagination(PageNumberPagination):
    """ Пагинация. """
    page_size = PAGE_SIZE
    page_size_query_param = 'limit'
