from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.urls import include, path
from django.utils.translation import ugettext_lazy as _
import groups.views as group_views
import debug_toolbar


admin.site.site_header = "Olympiad-helper"
admin.site.site_title = _("Olympiad-helper administration")
admin.site.index_title = _("Welcome to Olympiad-helper administration zone")


urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
    path('<str:short_id>/', group_views.redirect_to_full_url),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


urlpatterns += i18n_patterns(
    path('news/', include('news.urls')),
    path('admin/', admin.site.urls),
    path('judge/', include('judge.urls')),
    path('users/', include('users.urls')),
    path('groups/', include('groups.urls')),
    path('competitions/', include('competitions.urls')),
    path('linkshortening/', include('urlshortening.urls')),
)


if settings.DEBUG:
    urlpatterns.insert(0, path('__debug__/', include(debug_toolbar.urls)))