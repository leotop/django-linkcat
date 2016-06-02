from django.conf.urls import patterns, url
from linkcat.views import LinksHomeView, LinksCategoryView, LinksListView, switch_links_order, add_link_form, add_link_process_form, ModerationQueueView, moderate_confirm_action, moderate_link 


urlpatterns = [
    url(r'^link_added/(?P<slug>[-_\w]+)/$', add_link_process_form, name="links-add-link-process-form"),
    url(r'^add_link/(?P<slug>[-_\w]+)/$', add_link_form, name="links-add-link"),
    url(r'^list/(?P<slug>[-_\w]+)/$', LinksListView.as_view(), name="links-list"),
    url(r'^moderation/switch_links_order/(?P<link_pk_1>[0-9]+)/(?P<link_pk_2>[0-9]+)/$', switch_links_order, name="links-switch-links-order"),
    url(r'^moderation/confirm_moderate_link/(?P<id>[0-9]+)/(?P<action>[-_\w]+)/$', moderate_confirm_action, name="links-moderate-link-confirm"),
    url(r'^moderation/moderate_link/(?P<id>[0-9]+)/(?P<action>[-_\w]+)/$', moderate_link, name="links-moderate-link"),
    url(r'^moderation/$', ModerationQueueView.as_view(), name="links-moderation-queue"),
    url(r'^(?P<slug>[-_\w]+)/$', LinksCategoryView.as_view(), name="links-category-list"),
    url(r'^', LinksHomeView.as_view(), name="links-home"),
    ]

