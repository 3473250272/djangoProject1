from web import models
from django.shortcuts import render
from django import forms


# class CustomerForm(forms.ModelForm):
#     class Meta:
#         model = models.Customer
#         exclude = ['active', 'password']
#
#     def __init__(self, *args, **kwargs):
#         super(CustomerForm, self).__init__(*args, **kwargs)
#         # 设置所有字段为只读
#         for field in self.fields.values():
#             field.widget.attrs['readonly'] = True
#         self.fields['create_date'] = forms.DateTimeField(
#             label="注册日期",
#             initial=self.instance.create_date)


def my_space(request):
    query = models.Customer.objects.filter(id=request.user_data.user_id).select_related('level', 'creator')
    return render(request, 'web/my_space.html', {'query': query})
