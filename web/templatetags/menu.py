from django.conf import settings
import copy
from django import template

register = template.Library()


@register.inclusion_tag("tag/menu.html")
def nb_menu(request):
    user_menu_list = copy.deepcopy(settings.WEB_MENU[request.user_data.role])
    active_menu = None
    for item in user_menu_list:
        if item.get("children"):
            for child in item['children']:
                if child['url'] == request.path_info:
                    child['class'] = 'menu-active'
                    active_menu = item["text"]

    return {'menu_list': user_menu_list, 'active_menu': active_menu}
