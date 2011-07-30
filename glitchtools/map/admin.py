from django.contrib import admin

from glitchtools.map.models import Hub

class HubAdmin(admin.ModelAdmin):
    list_display = ('name', 'id')
    readonly_fields = ('id',)
    fields = ('id', 'name')
admin.site.register(Hub, HubAdmin)
