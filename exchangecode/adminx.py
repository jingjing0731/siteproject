import xadmin

from .models import Teacher

class TeacherAdmin(object):
    list_display = ['username','is_superuser','is_staff','phone_num','area','school']
    search_fields = ['username','phone_num']
    list_filter = ['area','school']
    list_per_page = 5

xadmin.site.unregister(Teacher)
xadmin.site.register(Teacher,TeacherAdmin)
