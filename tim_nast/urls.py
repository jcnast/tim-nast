from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from tim_nast import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'tim_nast.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^test/$', views.test),
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
