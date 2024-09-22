"""
如果想要以后使用分页，需要以下两个步骤：
在视图函数：
    def customer_list(request):
        # 所有数据
        queryset = models.Customer.objects.filter(active=1).select_related('level')

        pager = Pagination(request, queryset)
        context = {
            "queryset": queryset[pager.start:pager.end],
            "pager_string": obj.html()
        }
        return render(request, 'customer_list.html', context)

在页面上：
    {% for row in queryset %}
        {{row.id}}
    {% endfor %}

    <ul class="pagination">
        {{ pager_string }}
    </ul>
"""
import copy
from django.utils.safestring import mark_safe


class Pagination(object):
    """ 分页 """

    def __init__(self, request, query_set):

        self.query_dict = copy.deepcopy(request.GET)  # url携带的参数，默认禁止修改
        self.query_dict._mutable = True  # 设置允许
        self.limit = 10
        self.query_set = query_set  # 查询结果
        self.query_count = query_set.count()  # 数据长度
        self.page_count, div = divmod(self.query_count, self.limit)
        self.page_count = self.page_count + bool(div)  # 页面总数
        str_page = str(request.GET.get('page', 1))
        if not str_page.isdecimal():
            page = 1
        else:
            page = int(str_page)
            if page <= 0:
                page = 1
            else:
                if page > self.page_count:
                    page = self.page_count

        self.page = page
        self.current_case = None

        self.start = (page - 1) * self.limit
        self.end = page * self.limit

    def start_or_end(self, start):
        html_list = []
        if start:
            self.query_dict.setlist('page', [1])
            num = 1
        else:
            self.query_dict.setlist('page', [self.page_count])
            num = self.page_count
        html_list.append(
            '<li class="page-item"><a class="page-link" href="?{}">{}</a></li>'.format(self.query_dict.urlencode(),
                                                                                       num))
        return html_list

    def toggle_page(self, num):
        html_list = []
        self.query_dict.setlist('page', [self.page + num])
        if num > 0:
            if num == 1:
                text = '<i class="bi bi-chevron-right"></i>'
            else:
                text = '<i class="bi bi-chevron-double-right"></i>'
        else:
            if num == -1:
                text = '<i class="bi bi-chevron-left"></i>'
            else:
                text = '<i class="bi bi-chevron-double-left"></i>'
        html_list.append(
            '<li class="page-item"><a class="page-link" href="?{}">{}</a></li>'.format(self.query_dict.urlencode(),
                                                                                       text))
        return html_list

    def series_page(self, start_page, end_page):
        html_list = []
        for i in range(start_page, end_page + 1):
            self.query_dict.setlist('page', [i])
            if i == self.page:
                item = '<li class="page-item active" aria-current="page"><a class="page-link" href="?{}">{}</a></li>'.format(
                    self.query_dict.urlencode(), i)
            else:
                item = '<li class="page-item"><a class="page-link" href="?{}">{}</a></li>'.format(
                    self.query_dict.urlencode(), i)
            html_list.append(item)
        return html_list

    def html(self):
        if not self.page_count:
            return ""

        if self.page_count <= 11:  # 若内容不足以支撑最大容量
            center_start, center_end = 1, self.page_count
            self.current_case = 1  # 1~最后
        else:
            if self.page - 5 <= 1:
                center_start, center_end = 1, 10
                self.current_case = 2  # 1~10，··· ，end
            elif self.page + 5 >= self.page_count:
                center_start, center_end = self.page_count - 9, self.page_count
                self.current_case = 3  # 1，···，后10
            else:
                center_start, center_end = self.page - 4, self.page + 4
                self.current_case = 4  # 1，···，中间，···，end

        pager_list = []
        if self.page > 1:
            pager_list.extend(self.toggle_page(num=-1))
        else:
            pager_list.append(
                '<li class="page-item disabled"><a class="page-link" href="#"><i class="bi bi-chevron-left"></i></a></li>')

        if self.current_case in [3, 4]:
            pager_list.extend(self.start_or_end(True))
            pager_list.extend(self.toggle_page(num=-9))
        pager_list.extend(self.series_page(center_start, center_end))
        if self.current_case in [2, 4]:
            pager_list.extend(self.toggle_page(num=9))
            pager_list.extend(self.start_or_end(False))

        if self.page < self.page_count - 5:
            pager_list.extend(self.toggle_page(num=1))
        else:
            pager_list.append(
                '<li class="page-item disabled"><a class="page-link" href=""><i class="bi bi-chevron-right"></i></a></li>')

        pager_list.append(
            '<li class="page-item disabled" style="margin-left:30px"><span class="page-link">共{}条</span></li>'.format(
                self.query_count, self.page_count))

        pager_string = mark_safe("".join(pager_list))
        return pager_string

    def queryset(self):
        if self.query_count:
            return self.query_set[self.start:self.end]
        return self.query_set
