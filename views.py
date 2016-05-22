# -*- coding: utf-8 -*-

from django.core.urlresolvers import reverse
from django.http.response import Http404
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render_to_response
from django.views.generic import TemplateView, ListView, CreateView
from django.template import RequestContext
from django.views.generic.edit import FormView
from django.views.decorators.csrf import csrf_protect
from django.utils.html import strip_tags
from django.utils.translation import ugettext_lazy as _
from mcat.models import Category
from linkcat.models import Link
from linkcat.forms import AddLinkForm
from linkcat.conf import PAGINATE_BY, GROUPS_CAN_POST_LINK


class LinksHomeView(TemplateView):
    template_name = 'linkcat/index.html'

    def get_context_data(self, **kwargs):
        context = super(LinksHomeView, self).get_context_data(**kwargs)
        categories = Category.objects.filter(level__lte=0, status=0)
        context['categories'] = categories
        return context
    

class LinksCategoryView(TemplateView):
    template_name = 'linkcat/browse.html'

    def get_context_data(self, **kwargs):
        context = super(LinksCategoryView, self).get_context_data(**kwargs)
        current_category=get_object_or_404(Category, slug=self.kwargs['slug'])
        last_level=current_category.level+1
        categories = current_category.get_descendants().filter(level__lte=last_level, status=0)
        context['ancestors'] = current_category.get_ancestors()
        context['current_category'] = current_category
        context['categories'] = categories
        context['num_categories'] = len(categories)
        return context


class LinksListView(ListView):
    paginate_by = PAGINATE_BY
    context_object_name = 'links'
    template_name = 'linkcat/list.html'
    
    def get_queryset(self):
        self.category = get_object_or_404(Category, slug=self.kwargs['slug'], status=0)
        self.links = Link.objects.filter(category=self.category, status=0).order_by('created')
        return self.links
    
    def get_context_data(self, **kwargs):
        context = super(LinksListView, self).get_context_data(**kwargs)
        context['num_links'] = len(self.links)
        context['category'] = self.category
        context['ancestors'] = self.category.get_ancestors()
        return context


def add_link_form(request, slug):
    category = get_object_or_404(Category, slug=slug, status=0)
    if request.is_ajax():
        return render_to_response('linkcat/add_link_form.html',
                                    {'form': AddLinkForm(), 'category':category},
                                    context_instance=RequestContext(request),
                                    content_type="application/xhtml+xml"
                                    )
    else:
        raise Http404
    
@csrf_protect     
def add_link_process_form(request, slug):
    if request.is_ajax():
        if request.method == 'POST':
            # get the data
            url = strip_tags(request.POST['url'])
            name = strip_tags(request.POST['name'])
            description = strip_tags(request.POST['description'])
            # check if data is valid
            msg = ''
            status = None
            if not url:
                msg = _(u'Please provide an url')
                status = 'error'
            if not name:
                msg = _(u'Please provide a name for the link')
                status = 'error'
            # check user rights
            if request.user.is_anonymous():
                return HttpResponse('')
            else:
                link_status = 1
                if request.user.is_superuser or request.user.groups.filter(name__in=GROUPS_CAN_POST_LINK).exists():
                    # skip moderation
                    link_status = 0
                    msg = _(u'Link posted')
                    status = 'link_saved'
                else:
                    msg = _(u'Link saved for moderation. Thank you for your participation')
                    status = 'moderation'
                #category = get_object_or_404(Category, slug=slug, status=0)
                category = Category.objects.get(slug=slug, status=0)
                # check the data
                if not url.startswith('http://'):
                    msg = _(u'Please provide a valid url')
                    status = 'data_invalid'
                if not name:
                    msg = _(u'Please provide a name for the link')
                    status = 'data_invalid'
                # save link
                if status not in ['error', 'data_invalid']:
                    Link.objects.create(url=url, name=name, description=description, category=category, status=link_status, posted_by=request.user)
                return render_to_response('linkcat/add_link_success_message.html',
                            {'message':msg, 'status':status, 'category':category},
                            context_instance=RequestContext(request),
                            content_type="application/xhtml+xml"
                            )
        else:
            return HttpResponse('')
    else:
        raise Http404


