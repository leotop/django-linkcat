# -*- coding: utf-8 -*-

from django.contrib import admin
from linkcat.models import Link, LinksCategory


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


@admin.register(LinksCategory)
class LinksCategoryAdmin(admin.ModelAdmin):
    date_hierarchy = 'edited'
    fields = ['name', 'slug', 'parent', 'description', 'image', 'status', 'order']
    list_display = ['name', 'parent', 'created', 'edited', 'status']
    list_select_related = ['editor', 'parent']
    search_fields = ['name', 'editor__username']
    prepopulated_fields = {"slug": ("name",)}
    
    def save_model(self, request, obj, form, change):
        obj.editor = obj.posted_by = request.user
        return super(LinksCategoryAdmin, self).save_model(request, obj, form, change)