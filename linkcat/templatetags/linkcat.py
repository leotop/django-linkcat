# -*- coding: utf-8 -*-

from django import template
from ..models import Link


register = template.Library()

@register.filter
def next(some_list, current_index):
    """
    Returns the next element of the list using the current index if it exists.
    Otherwise returns an empty string.
    """
    try:
        return some_list[int(current_index) + 1] # access the next element
    except:
        return '' # return empty string in case of exception

@register.filter
def previous(some_list, current_index):
    """
    Returns the previous element of the list using the current index if it exists.
    Otherwise returns an empty string.
    """
    try:
        return some_list[int(current_index) - 1] # access the previous element
    except:
        return '' # return empty string in case of exception


class LastLinks(template.Node):
    
    def __init__(self, num_posts=10):
        links = Link.objects.filter().select_related('posted_by').order_by('-date')[:num_posts]
        links_ok = [] 
        for link in links:
            if link.status == 1:
                links_ok.append(link)
        self.links = links
        return
        
    def render(self, context):
        context['links'] = self.links
        return ''
    
def last_links(parser, token):
    return LastLinks()

register.tag('last_links', last_links)
