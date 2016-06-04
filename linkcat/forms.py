# -*- coding: utf-8 -*-

from django import forms
from linkcat.models import Link
        
      
class AddLinkForm(forms.ModelForm):
    class Meta:
        model = Link
        fields = ['url', 'name', 'description', 'language']
        widgets = {
            'description': forms.Textarea(attrs={'cols': 100, 'rows': 2, 'style':'width:100% !important;max-width:100% !important;'}),
            }


