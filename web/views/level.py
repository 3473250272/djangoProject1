from django.shortcuts import render, redirect
from web import models
from django.urls import reverse
from web.forms.forms import LevelModelForm


def level(request):
    queryset = models.Level.objects.filter(active=1).order_by('-percent')
    return render(request, 'web/level.html', {"queryset": queryset})


def level_add(request):
    if request.method == "GET":
        form = LevelModelForm()
        return render(request, 'web/data_form.html', {"form": form})

    form = LevelModelForm(data=request.POST)
    if not form.is_valid():
        return render(request, 'web/data_form.html', {"form": form})
    all_title = models.Level.objects.filter(active=1).values_list('title', flat=True)
    title = form.cleaned_data['title']
    if title in all_title:
        form.add_error('title', "该级别已存在")
        return render(request, 'web/data_form.html', {"form": form})
    form.save()
    return redirect(reverse('level'))


def level_edit(request, pk):
    level_object = models.Level.objects.filter(id=pk, active=1).first()

    if request.method == "GET":
        form = LevelModelForm(instance=level_object)
        return render(request, 'web/data_form.html', {"form": form})

    form = LevelModelForm(data=request.POST, instance=level_object)
    if not form.is_valid():
        return render(request, 'web/data_form.html', {"form": form})

    form.save()
    return redirect(reverse('level'))


def level_delete(request):
    cid = request.GET.get('cid', 0)
    exists = models.Customer.objects.filter(level_id=cid).exists()
    if not exists:
        models.Level.objects.filter(id=cid).update(active=0)
    return redirect(reverse('level'))
