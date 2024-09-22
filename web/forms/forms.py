import re
from utils.encrypt import md5
from utils.bootstrap import BootStrapForm
from django import forms
from web import models
from django_redis import get_redis_connection

username_regex = re.compile(r'^[\u4e00-\u9fa5a-zA-Z\d_-]{3,11}$')
phone_regex = re.compile(r'^1[3-9]\d{9}$')


class PwdForm(forms.Form):
    role = forms.ChoiceField(
        choices=(("2", "客户"), ("1", "管理员")),
        widget=forms.Select(attrs={'id': 'tab1-role', 'class': 'form-select'})
    )
    username_or_mobile = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '手机号/用户名'})
    )
    password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '密码'})
    )

    def clean_username_or_mobile(self):
        data = self.cleaned_data['username_or_mobile']
        if not data:
            raise forms.ValidationError("请输入您的用户名或手机号")

        if data.isdigit():
            if phone_regex.match(data):
                return data
            else:
                raise forms.ValidationError("请输入有效的手机号码")

        if not username_regex.match(data):
            raise forms.ValidationError("请输入有效的用户名")

        return data

    def clean_password(self):
        data = self.cleaned_data['password']
        if not data:
            raise forms.ValidationError("请输入账号的密码")
        return md5(data)


class SmsForm(forms.Form):
    role = forms.ChoiceField(
        choices=(("2", "客户端"), ("1", "管理端")),
        widget=forms.Select(attrs={'id': 'tab2-role', 'class': 'form-select'})
    )
    mobile = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '手机号'})
    )
    code = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '验证码'})
    )

    def clean_mobile(self):
        data = self.cleaned_data['mobile']
        if not data:
            raise forms.ValidationError("请输入您的手机号")

        if phone_regex.match(data):
            return data
        else:
            raise forms.ValidationError("请输入有效的手机号码")

    def clean_code(self):
        mobile = self.cleaned_data.get('mobile')
        code = self.cleaned_data['code']
        if not code:
            raise forms.ValidationError("验证码不能为空")

        conn = get_redis_connection("default")
        cache_code = conn.get(mobile)
        if not cache_code:
            raise forms.ValidationError("验证码未发送或已失效")

        if code != cache_code.decode("utf-8"):
            raise forms.ValidationError("验证码错误，请重新输入")
        return code


class MobileForm(forms.Form):
    mobile = forms.CharField(required=False)

    def clean_mobile(self):
        data = self.cleaned_data['mobile']
        if not data:
            raise forms.ValidationError("请输入您的手机号")

        if phone_regex.match(data):
            return data
        else:
            raise forms.ValidationError("请输入有效的手机号码")


class LevelModelForm(BootStrapForm, forms.ModelForm):
    class Meta:
        model = models.Level
        fields = ['title', 'percent']

    def clean_title(self):
        data = self.cleaned_data['title']
        if not data:
            raise forms.ValidationError("请输入级别")
        return data

    def clean_percent(self):
        data = self.cleaned_data['percent']
        if not data or not 0 <= data <= 100:
            raise forms.ValidationError("请输入折扣,范围为0~100（%）")
        return data


#  Customer model
class CustomerModelForm(BootStrapForm, forms.ModelForm):
    exclude_filed_list = ['level']
    confirm_password = forms.CharField(
        label="确认密码",
        widget=forms.PasswordInput(render_value=True)
    )

    class Meta:
        model = models.Customer
        fields = ["username", "mobile", "password", "confirm_password", "level"]
        widgets = {
            'password': forms.PasswordInput(render_value=True),
            'level': forms.Select(attrs={'class': 'form-select'})
        }

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 此处可能用到 request
        self.fields['level'].queryset = models.Level.objects.filter(active=1)

    def clean_password(self):
        password = self.cleaned_data['password']
        return md5(password)

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = md5(self.cleaned_data.get('confirm_password', ''))

        if password != confirm_password:
            raise forms.ValidationError("两次密码不一致")
        return confirm_password


class CustomerEditModelForm(BootStrapForm, forms.ModelForm):
    class Meta:
        model = models.Customer
        fields = ["username", 'mobile', 'level']
        widgets = {
            'password': forms.PasswordInput(render_value=True)
        }

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 此处可能用到 request
        self.fields['level'].queryset = models.Level.objects.filter(active=1)


class CustomerResetModelForm(BootStrapForm, forms.ModelForm):
    confirm_password = forms.CharField(
        label="重复密码",
        widget=forms.PasswordInput(render_value=True)
    )

    class Meta:
        model = models.Customer
        fields = ['password', 'confirm_password']
        widgets = {
            'password': forms.PasswordInput(render_value=True),
        }

    def clean_password(self):
        password = self.cleaned_data['password']

        return md5(password)

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = md5(self.cleaned_data.get('confirm_password', ''))

        if password != confirm_password:
            raise forms.ValidationError("密码不一致")
        return confirm_password


class ChargeModelForm(BootStrapForm, forms.ModelForm):
    # 静态变量
    charge_type = forms.TypedChoiceField(
        label="类型",
        choices=[(1, "充值"), (2, "扣款")],  # 只适合固定的数据，不适合去数据表中数据
        coerce=int
    )

    class Meta:
        model = models.TransactionRecord
        fields = ['charge_type', 'amount']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # self.fields['charge_type'].choices = [(1, "充值"), (2, "扣款")]  # 只适合固定的数据，不适合去数据表中数据
        # self.fields['creator'].choices = models.Administrator.objects.filter(id__gt=1).values_list("id", 'username')
