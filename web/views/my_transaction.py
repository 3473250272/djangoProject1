from django.shortcuts import render
from web import models
from utils.pager import Pagination
from django.db.models import Q
from utils.group import Option, NbSearchGroup


def my_transaction(request):
    """ 我的交易记录 """
    # 第一步：配置和传参
    search_group = NbSearchGroup(
        request,
        models.TransactionRecord,
        Option('charge_type'),  # choice
    )

    keyword = request.GET.get("keyword", "").strip()
    con = Q()
    if keyword:
        con.connector = 'OR'
        con.children.append(('order_oid__contains', keyword))

    # 第二步：获取条件 .filter(**search_group.get_condition)
    queryset = models.TransactionRecord.objects.filter(con).filter(**search_group.get_condition).filter(
        customer_id=request.user_data.user_id,
        active=1).order_by(
        "-id")
    pager = Pagination(request, queryset)

    context = {
        "pager": pager,
        "keyword": keyword,
        "search_group": search_group  # 第三步：传入前端页面
    }
    return render(request, 'web/my_transaction.html', context)


def transaction(request):
    # 第一步：配置和传参
    search_group = NbSearchGroup(
        request,
        models.TransactionRecord,
        Option('charge_type'),  # choice
    )

    keyword = request.GET.get("keyword", "").strip()
    con = Q()
    if keyword:
        con.connector = 'OR'
        con.children.append(('order_oid__contains', keyword))
        con.children.append(('customer__username__contains', keyword))

    # 第二步：获取条件 .filter(**search_group.get_condition)
    queryset = models.TransactionRecord.objects.filter(con).filter(**search_group.get_condition).filter(
        active=1).order_by("-id")
    pager = Pagination(request, queryset)

    context = {
        "pager": pager,
        "keyword": keyword,
        "search_group": search_group  # 第三步：传入前端页面
    }

    return render(request, "web/transaction.html", context)
