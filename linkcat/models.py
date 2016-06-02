# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _


class Presentation(models.Model):
    title = models.CharField(max_length=250, null=True, verbose_name=_(u'Title'))
    slug = models.SlugField(max_length=35, unique=True)
    debug_mode = models.BooleanField(default=False, verbose_name=_(u'Debug mode'))
    
    class Meta:
        ordering = ('title',)
        verbose_name = _(u'Presentation')
        verbose_name_plural = _(u'Presentations')

    def __unicode__(self):
        return unicode(self.title)


class Screen(models.Model):
    title = models.CharField(max_length=250, null=True, verbose_name=_(u'Title'))
    presentation = models.ForeignKey(Presentation, null=True, related_name='screen', verbose_name=_(u'Presentation'))
    order = models.PositiveSmallIntegerField(null=True, verbose_name=_(u'Order'))
    #~ images
    image_xl = models.ImageField(upload_to='fscreen', null=True, verbose_name=_(u'Image xl'))
    image_lg = models.ImageField(upload_to='fscreen', null=True, verbose_name=_(u'Image lg'))
    image_md = models.ImageField(upload_to='fscreen', null=True, verbose_name=_(u'Image md'))
    image_sm = models.ImageField(upload_to='fscreen', null=True, verbose_name=_(u'Image sm'))
    image_xs = models.ImageField(upload_to='fscreen', null=True, verbose_name=_(u'Image xs'))
    image_xxs = models.ImageField(upload_to='fscreen', null=True, verbose_name=_(u'Image xxs'))
    image_xxxs = models.ImageField(upload_to='fscreen', null=True, verbose_name=_(u'Image xxxs'))
    #~ html
    html_xl = models.TextField(null=True, blank=True, verbose_name=_(u'Html xl'))
    html_lg = models.TextField(null=True, blank=True, verbose_name=_(u'Html lg'))
    html_md = models.TextField(null=True, blank=True, verbose_name=_(u'Html md'))
    html_sm = models.TextField(null=True, blank=True, verbose_name=_(u'Html sm'))
    html_xs = models.TextField(null=True, blank=True, verbose_name=_(u'Html xs'))
    html_xxs = models.TextField(null=True, blank=True, verbose_name=_(u'Html xxs'))
    html_xxxs = models.TextField(null=True, blank=True, verbose_name=_(u'Html xxxs'))
    # breakpoints values
    xl_breakpoint = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name=_(u'Custom xl breakpoint'), default=1350, help_text=_(u'Value for the xl breakpoint in pixels'))
    lg_breakpoint = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name=_(u'Custom lg breakpoint'), default=1200, help_text=_(u'Value for the lg breakpoint in pixels'))
    md_breakpoint = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name=_(u'Custom md breakpoint'), default=1024, help_text=_(u'Value for the md breakpoint in pixels'))
    sm_breakpoint = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name=_(u'Custom sm breakpoint'), default=768, help_text=_(u'Value for the sm breakpoint in pixels'))
    xs_breakpoint = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name=_(u'Custom xs breakpoint'), default=640, help_text=_(u'Value for the xs breakpoint in pixels'))
    xxs_breakpoint = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name=_(u'Custom xxs breakpoint'), default=480, help_text=_(u'Value for the xxs breakpoint in pixels'))
    xxxs_breakpoint = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name=_(u'Custom xxxs breakpoint'), default=360, help_text=_(u'Value for the xxxs breakpoint in pixels'))
    
    
    class Meta:
        order_with_respect_to = 'presentation'
        verbose_name = _(u'Screen')
        verbose_name_plural = _(u'Screens')

    def __unicode__(self):
        return unicode(self.title)
    