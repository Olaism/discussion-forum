from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("accounts.urls")),
    path("accounts/", include("django.contrib.auth.urls")),
    path('blog/', include("blog.urls", namespace='blog')),
    path("boards/", include("boards.urls")),
    path("", RedirectView.as_view(url="/boards/")),
]
