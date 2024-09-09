from rest_framework.filters import SearchFilter


class CustomSearchFilter(SearchFilter):
    search_description = 'Enter a name to search for'
