import random
from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse
from web.forms.forms import PwdForm, SmsForm, MobileForm
from web.models import Administrator, Customer
from django_redis import get_redis_connection
from django.conf import settings
from utils.response import BaseResponse
from django.db.models import Q

mapping = {"1": "ADMIN", "2": "CUSTOMER"}


# Create your views here.
def login(request):
    if request.method == "GET":
        return _render_login_page(request)
    login_way = request.POST.get("way")
    role = request.POST.get('role')
    if login_way == "pwd" and role in mapping:
        return _handle_pwd_login(request, role)
    elif login_way == "sms" and role in mapping:
        return _handle_sms_login(request, role)
    return _render_login_page(request)


# 渲染登录页面
def _render_login_page(request, form1=None, form2=None, index=1):
    if form1 is None:
        form1 = PwdForm()
    if form2 is None:
        form2 = SmsForm()
    return render(request, 'web/login.html', {'form1': form1, 'form2': form2, 'index': index})


#  处理账号登录
def _handle_pwd_login(request, role):
    form1 = PwdForm(data=request.POST)
    form2 = SmsForm()
    if not form1.is_valid():
        return _render_login_page(request, form1=form1, form2=form2, index=1)  # 重定向

    form1_dict = form1.cleaned_data
    user_object = _authenticate_user(form1_dict['username_or_mobile'], form1_dict['password'], role)
    if not user_object:
        form1.add_error('password', "账号或密码错误")
        return _render_login_page(request, form1=form1, form2=form2, index=1)
    request.session[settings.WEB_SESSION_KEY] = {'role': mapping[role], 'name': user_object.username,
                                                 'user_id': user_object.id}
    return redirect('home')


#  处理短信登录
def _handle_sms_login(request, role):
    form1 = PwdForm()
    form2 = SmsForm(data=request.POST)
    if not form2.is_valid():
        return _render_login_page(request, form1=form1, form2=form2, index=0)
    mobile = form2.cleaned_data['mobile']
    if role == '1':
        port = "管理端"
        user_object = Administrator.objects.filter(active=1, mobile=mobile).first()
    else:
        port = "客户端"
        user_object = Customer.objects.filter(active=1, mobile=mobile).first()

    if not user_object:
        form2.add_error('mobile', f'该账户未注册{port}')
        return _render_login_page(request, form1=form1, form2=form2, index=0)
    request.session[settings.WEB_SESSION_KEY] = {'role': mapping[role], 'name': user_object.username,
                                                 'user_id': user_object.id}
    return redirect('home')


#  返回账号登录匹配结果
def _authenticate_user(userid, password, role):
    if role == "1":
        return Administrator.objects.filter(
            Q(active=1) & (Q(username=userid) | Q(mobile=userid)) | Q(password=password)).first()
    else:
        return Customer.objects.filter(
            Q(active=1) & (Q(username=userid) | Q(mobile=userid)) | Q(password=password)).first()


def sms_send(request):
    """验证手机号"""
    res = BaseResponse()
    form = MobileForm(data=request.POST)
    if not form.is_valid():
        res.detail = form.errors  # 提交错误
        return JsonResponse(res.dict, json_dumps_params={'ensure_ascii': False})

    """生成验证码"""
    mobile = form.cleaned_data['mobile']
    # sms_code = str(random.randint(0000, 9999))
    sms_code = str(1234)

    """发送验证码"""
    # 暂时跳过短信发送平台
    is_success = True
    if not is_success:
        res.detail = {"mobile": ["发送失败，请稍后重试"]}  # 提交错误
        return JsonResponse(res.dict, json_dumps_params={"ensure_ascii": False})

    """redis内设置验证码"""
    conn = get_redis_connection("default")
    conn.set(mobile, sms_code, ex=300)
    res.status = True
    res.detail = {"mobile": ["发送成功,请注意查收"]}
    return JsonResponse(res.dict)


def home(request):
    return render(request, 'web/home.html')


def logout(request):
    request.session.clear()
    return redirect(settings.WEB_LOGIN_URL)
