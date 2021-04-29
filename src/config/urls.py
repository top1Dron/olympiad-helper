from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.urls import include, path
import groups.views as group_views
 
urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
    path('<str:short_id>/', group_views.redirect_to_full_url),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


urlpatterns += i18n_patterns(
    path('', include('news.urls')),
    path('admin/', admin.site.urls),
    path('judge/', include('judge.urls')),
    path('users/', include('users.urls')),
    path('groups/', include('groups.urls')),
    path('competitions/', include('competitions.urls')),
    path('linkshortening/', include('urlshortening.urls')),
)
