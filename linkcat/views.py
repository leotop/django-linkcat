# -*- coding: utf-8 -*-

from django.http import Http404, HttpResponse
from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404
from fscreen.models import Presentation
from fscreen.utils import get_slide


class PresentationView(TemplateView): 
    template_name = "fscreen/index.html"
    
    def get_context_data(self, **kwargs):
        context = super(PresentationView, self).get_context_data(**kwargs)
        presentation = get_object_or_404(Presentation, slug=self.kwargs['slug'])
        context['presentation'] = presentation
        context['screen_number'] = 1
        return context


class ScreenLoader(TemplateView): 
    template_name = "fscreen/screen.html"
    
    def get_context_data(self, **kwargs):
        if self.request.is_ajax():
            context = super(ScreenLoader, self).get_context_data(**kwargs)
            try:
                screen_number = int(kwargs['screen_number']) - 1
                presentation = Presentation.objects.filter(slug=self.kwargs['presentation_slug']).prefetch_related('screen')[0]
            except Presentation.DoesNotExist:
                return HttpResponse('')
            screen = presentation.screen.all().order_by('order')[screen_number]
            screen_width = int(kwargs['screen_width'])
            image, html = get_slide(screen, screen_width)
            context['presentation'] = presentation
            context['image'] = image
            context['html'] = html
            return context
        else:
            raise Http404
