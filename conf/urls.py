from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path

from blog.sitemaps import PostSiteMap


sitemaps = {
    'posts': PostSiteMap
}


urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("accounts.urls")),
    path("accounts/", include("django.contrib.auth.urls")),
    path('blog/', include("blog.urls", namespace='blog')),
    path('api/v1/blogs/', include("blog.api.urls", namespace='blog-api')),
    path("boards/", include("boards.urls")),
    path("", include("pages.urls", namespace='pages')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap')
]
