from django.utils.translation import ugettext_lazy as _
from django.apps import AppConfig

class LinkcatConfig(AppConfig):
    name = "linkcat"
    verbose_name = _(u"Links catalog")
    
    def ready(self):
        pass