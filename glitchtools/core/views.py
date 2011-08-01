from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse

def comingsoon(request):
    return HttpResponseRedirect(request.build_absolute_uri('/map/'))
    return TemplateResponse(request, 'glitchtools/core/comingsoon.html', {})
