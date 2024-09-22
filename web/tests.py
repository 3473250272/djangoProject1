query_set = [i for i in range(17)]
query_count = query_set.__len__()

limit = 10
page_count, div = divmod(query_count, limit)

page = 2
page_start = (page - 1) * limit
page_end = page * limit

page_show = query_set[page_start: page_end]
print("第{}页：".format(page) + str(page_show))
