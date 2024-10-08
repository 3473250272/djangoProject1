# 启动django
import os
import sys
import django

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangoProject1.settings')
django.setup()  # 伪造让django启动

from web import models
from utils.encrypt import md5

# 创建级别
# level_object = models.Level.objects.create(title="VIP", percent=90)

# models.Customer.objects.create(
#     username='xinchen',
#     password=md5("xinchen"),
#     mobile='19912341234',
#     level_id=1,
#     creator_id=1
# )
for i in range(1, 302):
    models.Customer.objects.create(
        username='xinchen-{}'.format(i),
        password=md5("xinchen-{}".format(i)),
        mobile='19912341234',
        level_id=1,
        creator_id=1
    )
