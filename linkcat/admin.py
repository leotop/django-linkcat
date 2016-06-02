# -*- coding: utf-8 -*-

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from codemirror2.widgets import CodeMirrorEditor
from fscreen.models import Presentation, Screen
  

@admin.register(Screen)
class ScreenAdmin(admin.ModelAdmin):
    save_as = True
    list_display= ('title','get_presentation_name','order')
    search_fields = ['presentation__title', 'title']
    fieldsets = (
        (None, {
            'fields': ('title','presentation','order')
        }),
        ('Xl', {
            'classes': ('collapse',),
            'fields': ('xl_breakpoint','image_xl','html_xl')
        }),
        ('Lg', {
            'classes': ('collapse',),
            'fields': ('image_lg','html_lg')
        }),
        ('Md', {
            'classes': ('collapse',),
            'fields': ('image_md','html_md')
        }),
        ('Sm', {
            'classes': ('collapse',),
            'fields': ('image_sm','html_sm')
        }),
        ('Xs', {
            'classes': ('collapse',),
            'fields': ('image_xs','html_xs')
        }),
        ('Custom xxs', {
            'classes': ('collapse',),
            'fields': ('xxs_breakpoint','image_xxs','html_xxs')
        }),
        ('Custom xxxs', {
            'classes': ('collapse',),
            'fields': ('xxxs_breakpoint','image_xxxs','html_xxxs')
        })
    )
    
    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.attname in ["html_xl", "html_lg", "html_md", "html_sm", "html_xs", "html_xxs", "html_xxxs"]:
            kwargs['widget'] = CodeMirrorEditor(
                                                options={
                                                         'mode': 'htmlmixed',
                                                         'indentWithTabs':'true',
                                                         'lineNumbers':'true',
                                                         'autoCloseTags': 'true',
                                                         'theme':'blackboard',
                                                         'styleActiveLine': 'true',
                                                         'indentUnit' : '4',
                                                        }, 
                                                modes=['css', 'xml', 'javascript', 'htmlmixed']
                                                )
        return super(ScreenAdmin, self).formfield_for_dbfield(db_field, **kwargs)
    
    def get_presentation_name(self, obj):
        return obj.presentation.title
    
    get_presentation_name.admin_order_field  = 'presentation'
    get_presentation_name.short_description = _(u'Presentation')

@admin.register(Presentation)
class PresentationAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    
