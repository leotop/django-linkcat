# -*- coding: utf-8 -*-

from django.utils.translation import ugettext_lazy as _

from django.apps import AppConfig


class FscreenConfig(AppConfig):
    name = 'fscreen'
    verbose_name = _(u"Fullscreen slides")
    
    def ready(self):
        pass