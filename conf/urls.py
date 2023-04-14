from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("accounts.urls")),
    path("accounts/", include("django.contrib.auth.urls")),
    path('blog/', include("blog.urls", namespace='blog')),
    path("boards/", include("boards.urls")),
    path("", include("pages.urls", namespace='pages')),
]
