from django import template
from django.db.models import Count

from ..models import Sermon

register = template.Library()


@register.inclusion_tag('latest_sermons.html')
def show_latest_sermons():
    latest_sermons = Sermon.objects.filter(status='publish').order_by('-publish')[:3]
    return {'latest_sermons': latest_sermons}
