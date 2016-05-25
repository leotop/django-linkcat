# -*- coding: utf-8 -*-

from django.db import models
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from mptt.models import TreeForeignKey, MPTTModel
from mbase.models import MetaBaseModel, MetaBasePostedByModel, MetaBaseStatusModel, MetaBaseNameModel, OrderedModel, MetaBaseUniqueSlugModel


class LinksCategory(MPTTModel, MetaBaseModel, MetaBaseNameModel, MetaBaseStatusModel, MetaBaseUniqueSlugModel, OrderedModel):
    parent = TreeForeignKey('self', null=True, blank=True, related_name=u'children', verbose_name=_(u'Parent category'))
    image = models.ImageField(null=True, upload_to='categories', verbose_name=_(u"Navigation image"))
    description = models.TextField(blank=True, verbose_name=_(u'Description'))
    
    
    class Meta:
        verbose_name=_(u'Category')
        verbose_name_plural = _(u'Categories')
        ordering = ('order',)

    def __unicode__(self):
        return unicode(self.name)


class Link(MetaBaseModel, MetaBaseStatusModel, MetaBasePostedByModel):
    url = models.URLField(verbose_name=_(u'Url'))
    name = models.CharField(max_length=200, verbose_name=_(u'Name'))
    description = models.TextField(blank=True, verbose_name=_(u'Description'))
    category = models.ForeignKey(LinksCategory, verbose_name=_(u'Category'))
    
    class Meta:
        verbose_name=_(u'Link')
        verbose_name_plural = _(u'Links')
        ordering = ('-created',)

    def __unicode__(self):
        return unicode(self.url)
    
    def __str__(self):
        return self.url.encode('utf8')
    
    def get_absolute_url(self):
        return reverse('links-list', kwargs={'slug':self.category.slug})
    
    def save(self, *args, **kwargs):
        # limit the number of caracters for description
        self.description = self.description[:350]
        return super(Link, self).save(*args, **kwargs)