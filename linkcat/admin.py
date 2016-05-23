# -*- coding: utf-8 -*-

from django.contrib import admin
from linkcat.models import Link


@admin.register(Link)
class LinkAdmin(admin.ModelAdmin):
    date_hierarchy = 'edited'
    fields = ['url', 'name', 'description', 'category', 'posted_by', 'editor', 'created', 'edited']
    readonly_fields = [ 'posted_by', 'editor', 'edited', 'created' ]
    list_display = ['url', 'category', 'posted_by', 'created', 'edited', 'status']
    list_select_related = ['editor', 'posted_by']
    search_fields = ['url', 'posted_by__username', 'editor__username']
    
    def save_model(self, request, obj, form, change):
        obj.editor = obj.posted_by = request.user
        return super(LinkAdmin, self).save_model(request, obj, form, change)