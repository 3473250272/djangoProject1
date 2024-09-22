from django.shortcuts import redirect, HttpResponse
from django.utils.deprecation import MiddlewareMixin
from django.conf import settings
from django.http import JsonResponse


class UserInfo(object):
    def __init__(self, role, name, user_id):
        self.role = role
        self.name = name
        self.user_id = user_id
        self.menu_name = None
        self.text_list = []


class AuthMiddleware(MiddlewareMixin):
    def is_white_info(self, request):
        if request.path_info in settings.WEB_WHITE_URL:
            return True

    def process_request(self, request):
        """校验用户是否已登录"""
        if self.is_white_info(request):
            return

        user_dict = request.session.get(settings.WEB_SESSION_KEY)
        if not user_dict:
            return redirect(settings.WEB_LOGIN_URL)

        request.user_data = UserInfo(**user_dict)

    def process_view(self, request, callback, callback_args, callback_kwargs):
        if self.is_white_info(request):
            return
        current_name = request.resolver_match.url_name
        if current_name in settings.NB_PERMISSION_PUBLIC:
            return
        # 获取用户具备的权限
        all_dict = {**settings.NB_PERMISSION_PUBLIC, **settings.NB_PERMISSION[request.user_data.role]}

        # 判断URL是否在当前用户权限中
        if current_name not in all_dict:
            if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
                return JsonResponse({'status': False, 'detail': '无权访问'})
            else:
                return HttpResponse("无权访问")
        text_list = [all_dict[current_name]['text']]
        menu_name = current_name
        # 逆向匹配完整url
        while all_dict[menu_name]['parent']:
            menu_name = all_dict[menu_name]['parent']
            text_list.append(all_dict[menu_name]['text'])

        text_list.reverse()
        request.user_data.menu_name = menu_name  # 当前url对应菜单
        request.user_data.text_list = text_list
