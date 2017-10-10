from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    url(r'^$', views.post_list, name='post_list'),
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<post>[-\w]+)/$',
        views.post_detail, name='post_detail'),
    url(r'^(?P<post_id>\d+)/share/$', views.post_share,
        name='post_share'),
    url(r'^testing/$', views.testing, name='testing')
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

