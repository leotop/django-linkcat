from django.conf.urls import patterns, url
from fscreen.views import ScreenLoader, PresentationView


urlpatterns = patterns('',
    url(r'^loader/(?P<presentation_slug>[-_\w]+)/(?P<screen_number>[0-9]+)/(?P<screen_width>[0-9]+)/$', ScreenLoader.as_view(), name='screen-loader'),
    url(r'^(?P<slug>[-_\w]+)/$', PresentationView.as_view(), name='presentation-home'),
)