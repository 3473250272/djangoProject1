from django.shortcuts import render, redirect
from web import models
from utils.pager import Pagination
from django import forms
from utils.bootstrap import BootStrapForm
from utils.response import BaseResponse
from django.http import JsonResponse


def policy(request):
    queryset = models.PricePolicy.objects.all().order_by('count')
    pager = Pagination(request, queryset)
    return render(request, 'web/policy.html', {'pager': pager})


class PolicyModelForm(BootStrapForm, forms.ModelForm):
    class Meta:
        model = models.PricePolicy
        fields = "__all__"


def policy_add(request):
    if request.method == "GET":
        form = PolicyModelForm()
        return render(request, 'web/data_form.html', {'form': form})
    form = PolicyModelForm(data=request.POST)
    if not form.is_valid():
        return render(request, 'web/data_form.html', {'form': form})
    form.save()
    return redirect('/policy/')


def policy_edit(request, pk):
    instance = models.PricePolicy.objects.filter(id=pk).first()
    if request.method == "GET":
        form = PolicyModelForm(instance=instance)
        return render(request, 'web/data_form.html', {'form': form})
    form = PolicyModelForm(data=request.POST, instance=instance)
    if not form.is_valid():
        return render(request, 'web/data_form.html', {'form': form})
    form.save()
    # return redirect('/policy/list/')
    from utils.link import filter_reverse
    return redirect(filter_reverse(request, "/policy/"))


def policy_delete(request):
    res = BaseResponse(status=True)
    cid = request.GET.get('cid')
    models.PricePolicy.objects.filter(id=cid).delete()
    return JsonResponse(res.dict)
