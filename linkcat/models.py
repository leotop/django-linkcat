# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _
from mcat.models import Category
from mbase.models import MetaBaseModel, MetaBasePostedByModel, MetaBaseStatusModel


class Link(MetaBaseModel, MetaBaseStatusModel, MetaBasePostedByModel):
    url = models.URLField(verbose_name=_(u'Url'))
    name = models.CharField(max_length=200, verbose_name=_(u'Name'))
    description = models.TextField(blank=True, verbose_name=_(u'Description'))
    category = models.ForeignKey(Category, verbose_name=_(u'Category'))
    
    class Meta:
        verbose_name=_(u'Link')
        verbose_name_plural = _(u'Links')
        ordering = ('-created',)

    def __unicode__(self):
        return unicode(self.url)