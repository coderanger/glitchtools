from django.contrib import admin
from glitchtools.users.models import GlitchUser

class GlitchUserAdmin(admin.ModelAdmin):
    pass
admin.site.register(GlitchUser, GlitchUserAdmin)
