from django.conf.urls import patterns, url
from linkcat.views import LinksHomeView, LinksCategoryView, LinksListView, add_link_form, add_link_process_form


urlpatterns = [
    url(r'^link_added/(?P<slug>[-_\w]+)/$', add_link_process_form, name="links-add-link-process-form"),
    url(r'^add_link/(?P<slug>[-_\w]+)/$', add_link_form, name="links-add-link"),
    url(r'^list/(?P<slug>[-_\w]+)/$', LinksListView.as_view(), name="links-list"),
    url(r'^(?P<slug>[-_\w]+)/$', LinksCategoryView.as_view(), name="links-category-list"),
    url(r'^', LinksHomeView.as_view(), name="links-home"),
    ]

