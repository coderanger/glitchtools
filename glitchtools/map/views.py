from django.template.response import TemplateResponse

from glitchtools.map.models import Hub, Street

def index(request):
    data = {
        'hubs': Hub.objects.all().order_by('name'),
        'streets': Street.objects.all().order_by('name'),
        'current_location': '',
    }
    if request.glitch_user and request.glitch_user.location:
        data['current_location'] = Street.objects.filter(tsid=request.glitch_user.location).values('tsid', 'name')
    return TemplateResponse(request, 'glitchtools/map/index.html', data)

