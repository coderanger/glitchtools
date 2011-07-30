from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from glitchtools.users.models import GlitchUser

class GlitchUserAdmin(admin.ModelAdmin):
    list_display = ('name', 'tsid', 'scope')

    def name(self, obj):
        return obj.user.username
    name.short_description = _('Username')
admin.site.register(GlitchUser, GlitchUserAdmin)
