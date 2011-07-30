from django.template.response import TemplateResponse

def comingsoon(request):
    return TemplateResponse(request, 'glitchtools/core/comingsoon.html', {})
