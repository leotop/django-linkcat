from django.conf.urls import url
from linkcat.views import LinksAndCategoriesView, LinksHomeView, switch_links_order, add_link_form, add_link_process_form, ModerationQueueView, moderate_confirm_action, moderate_link, view_links  


urlpatterns = [
    url(r'^link_added/(?P<slug>[-_\w]+)/$', add_link_process_form, name="links-add-link-process-form"),
    url(r'^add_link/(?P<slug>[-_\w]+)/$', add_link_form, name="links-add-link"),
    url(r'^moderation/switch_links_order/(?P<link_pk_1>[0-9]+)/(?P<link_pk_2>[0-9]+)/$', switch_links_order, name="links-switch-links-order"),
    url(r'^moderation/confirm_moderate_link/(?P<id>[0-9]+)/(?P<action>[-_\w]+)/$', moderate_confirm_action, name="links-moderate-link-confirm"),
    url(r'^moderation/moderate_link/(?P<id>[0-9]+)/(?P<action>[-_\w]+)/$', moderate_link, name="links-moderate-link"),
    url(r'^moderation/$', ModerationQueueView.as_view(), name="links-moderation-queue"),
    url(r'^load_link_list/(?P<slug>[-_\w]+)/$', view_links, name="links-load-list"),
    url(r'^(?P<slug>[-_\w]+)/$', LinksAndCategoriesView.as_view(), name="links-category-list"),
    url(r'^', LinksHomeView.as_view(), name="links-home"),
    ]

