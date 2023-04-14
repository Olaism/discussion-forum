from django.urls import path
from django.views.generic import RedirectView

from .views import SearchResultsView

app_name = 'pages'

urlpatterns = [
    path('search/', SearchResultsView.as_view(), name='search_results'),
    path("", RedirectView.as_view(url="/boards/")),
]
