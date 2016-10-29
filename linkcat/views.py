# -*- coding: utf-8 -*-

from django.core.urlresolvers import reverse
from django.core.paginator import Paginator
from django.http.response import Http404
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.views.generic import TemplateView, ListView, CreateView
from django.template import RequestContext
from django.views.generic.edit import FormView
from django.views.decorators.csrf import csrf_protect
from django.utils.html import strip_tags
from django.utils.translation import ugettext_lazy as _
from braces.views import GroupRequiredMixin
from linkcat.models import LinksCategory as Category
from linkcat.models import Link
from linkcat.forms import AddLinkForm
from linkcat.conf import PAGINATE_BY, GROUPS_CAN_MODERATE, DEFAULT_LANGUAGE
from linkcat.utils import is_moderator, can_post_link


class LinksHomeView(TemplateView):
    template_name = 'linkcat/index.html'

    def get_context_data(self, **kwargs):
        context = super(LinksHomeView, self).get_context_data(**kwargs)
        categories = Category.objects.filter(level__lte=0, status=0)
        num_links = Link.objects.all().count()
        is_modo = is_moderator(self.request.user)
        if is_modo:
            num_items_in_queue = Link.objects.filter(status=1).count()
            context['num_items_in_queue'] = num_items_in_queue
        context['is_moderator'] = is_modo
        context['categories'] = categories
        context['num_links'] = num_links 
        return context
  

class LinksAndCategoriesView(ListView):
    context_object_name = 'links'
    
    def get_queryset(self):
        self.category = get_object_or_404(Category, slug=self.kwargs['slug'], status=0)
        self.links = Link.objects.filter(category=self.category, status=0).order_by('order')
        return self.links
    
    def get_template_names(self):
        if self.request.is_ajax():
            template_name = 'linkcat/list_ajax.html'
        else:
            template_name = 'linkcat/listcat.html'
        return [template_name]
    
    def get_context_data(self, **kwargs):
        context = super(LinksAndCategoriesView, self).get_context_data(**kwargs)
        edit_mode = False
        last_level = self.category.level+1
        categories = self.category.get_descendants().filter(level__lte=last_level, status=0)
        ancestors = self.category.get_ancestors()
        parent = None
        if len(ancestors) > 0:
            parent = ancestors.reverse()[0]
        edit_mode = False
        context['categories'] = categories.order_by('order')
        if self.request.GET.has_key('edit_mode'):
            context['edit_mode'] = True
        context['is_moderator'] = is_moderator(self.request.user)
        context['num_links'] = len(self.links)
        context['category'] = self.category
        context['ancestors'] = ancestors
        context['parent'] = parent
        context['links'] = self.links
        context['default_language'] = DEFAULT_LANGUAGE
        return context

class ModerationQueueView(ListView, GroupRequiredMixin):
    group_required = GROUPS_CAN_MODERATE
    paginate_by = PAGINATE_BY
    context_object_name = 'links'
    template_name = 'linkcat/moderation/queue.html'
    
    def get_queryset(self):
        qs = Link.objects.filter(status=1).select_related('category', 'posted_by').order_by('-created')
        return qs


# ------------------------------- ajax stuff -----------------------------------
def view_links(request, slug):
    if request.is_ajax():
        category = get_object_or_404(Category, slug=slug, status=0)
        links = Link.objects.filter(category=category, status=0).order_by('order')
        return render(request, 'linkcat/list_ajax.html',
                                    {'links':links, 'num_links':len(links), 'category':category},
                                    content_type="application/xhtml+xml"
                                    )
    else:
        raise Http404

def moderate_confirm_action(request, id, action):
    if request.is_ajax():
        # check rights to mmoderate
        is_modo = is_moderator(request.user)
        if is_modo is False:
            return HttpResponse('')
        return render(request, 'linkcat/moderation/moderate_link_confirm.html',
                                    {'id':id, 'action':action},
                                    content_type="application/xhtml+xml"
                                    )
    else:
        raise Http404

def moderate_link(request, id, action):
    if request.is_ajax():
        # check rights to moderate
        is_modo = is_moderator(request.user)
        if is_modo is False:
            return HttpResponse('')
        # get the link
        try:
            link = Link.objects.get(pk=int(id))
        except:
            return HttpResponse('Error: link not found')
        # process action
        if action == 'accept':
            link.status = 0
            link.save()
        elif action == 'reject':
            link.delete()
        return render(request, 'linkcat/moderation/link_moderated.html',
                                  {'id':id},
                                    content_type="application/xhtml+xml"
                                    )
    else:
        raise Http404


def add_link_form(request, slug):
    category = get_object_or_404(Category, slug=slug, status=0)
    if request.is_ajax():
        return render(request, 'linkcat/add_link_form.html',
                                    {'form': AddLinkForm(), 'category':category},
                                    content_type="application/xhtml+xml"
                                    )
    else:
        raise Http404
    
@csrf_protect     
def add_link_process_form(request, slug):
    if request.is_ajax():
        # check user rights
        if request.user.is_anonymous():
            return HttpResponse('')
        if request.method == 'POST':
            # get the data
            url = strip_tags(request.POST['url'])
            name = strip_tags(request.POST['name'])
            description = strip_tags(request.POST['description'])
            language = strip_tags(request.POST['language'])
            # check if data is valid
            msg = ''
            status = None
            if not url:
                msg = _(u'Please provide a valid url')
                status = 'data_invalid'
            if not name and url:
                msg = _(u'Please provide a name for the link')
                status = 'data_invalid'
            link_status = 1
            category = Category.objects.filter(slug=slug, status=0).prefetch_related('links')[0]
            if status != 'data_invalid':
                if can_post_link(request.user):
                    # skip moderation
                    link_status = 0
                    msg = _(u'Link posted')
                    status = 'link_saved'
                else:
                    msg = _(u'Link saved for moderation. Thank you for your participation')
                    status = 'moderation'
                # auto set order
                links = category.links.all()
                if len(links) > 0:
                    order = links.latest('order').order+10
                else:
                    order = 10
                # save link
                link = Link.objects.create(url=url, name=name, description=description, category=category, status=link_status, posted_by=request.user, order=order, language=language)
            return render(request, 'linkcat/add_link_success_message.html',
                        {'message':msg, 'status':status, 'link':link, 'category':category},
                        content_type="application/xhtml+xml"
                        )
        else:
            return HttpResponse('')
    else:
        raise Http404
    
    
def switch_links_order(request, link_pk_1, link_pk_2):
    if request.is_ajax():
        # check rights to moderate
        is_modo = is_moderator(request.user)
        if is_modo is False:
            return HttpResponse('')
        # get the objects
        try:
            links = Link.objects.filter(pk__in=[link_pk_1,link_pk_2]).select_related('category').order_by('order')
        except Link.ObjectDoesNotExist:
            return HttpResponse('')
        link1 = links.filter(pk=link_pk_1)[0]
        link2 = links.filter(pk=link_pk_2)[0]
        category = link1.category
        link1_order = link1.order
        link2_order = link2.order
        print str(link1.order)+' / '+str(link2.order)
        # switdh order
        link1.order = link2_order
        link2.order = link1_order
        link1.save()
        link2.save()
        return HttpResponseRedirect(reverse('links-category-list', kwargs={'slug': category.slug})+'?edit_mode=1')
    else:
        raise Http404