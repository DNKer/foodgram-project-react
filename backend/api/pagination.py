from rest_framework.pagination import PageNumberPagination

from django.conf import settings


class LimitPageNumberPagination(PageNumberPagination):
    """ Пагинация. """
    page_size = settings.DEFAULT_PAGE_SIZE
    page_size_query_param = 'limit'
