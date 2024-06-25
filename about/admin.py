from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import About
# Register your models here.

@admin.register(About)
class AboutAdmin(SummernoteModelAdmin):
    summernote_fields = ('content',)