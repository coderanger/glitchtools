from django.contrib import admin
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from glitchtools.map.models import Hub, Street

class HubAdmin(admin.ModelAdmin):
    list_display = ('name', 'id')
    readonly_fields = ('id',)
    fields = ('id', 'name')


class StreetAdmin(admin.ModelAdmin):
    list_display = ('name', 'hub', 'tsid')
    readonly_fields = ('connections_summary',)
    fieldsets = (
        (None, {
            'fields': ('name', 'hub', 'tsid')
        }),
        (_('Connections'), {
            'fields': ('connections_summary', 'connections'),
        }),
        (_('Tracking information'), {
            'classes': ('collapse',),
            'fields': ('deleted', 'last_update')
        }),
    )

    def connections_summary(self, obj):
        return ', '.join('<a href="%s">%s</a>'%(reverse('admin:map_street_change', args=(street.id,)), street.name) for street in obj.connections.all())
    connections_summary.short_description = _('connection summary')
    connections_summary.allow_tags = True

admin.site.register(Hub, HubAdmin)
admin.site.register(Street, StreetAdmin)
