from rest_framework import routers
from rest_framework_simplejwt.views import token_obtain_pair

from exchangecode import views

from django.urls import path,re_path
from rest_framework import routers


from .views import batch, teacher, code, login,area,school

urlpatterns=[
    # #batch批次
    # path("batch/create/",batch.CreateBatch.as_view()),
    # path("batch/", batch.ListBatch.as_view()),
    # re_path(r"^batch/(?P<pk>\d+)/$", batch.RetrieveUpdateDestroyListBatch.as_view()),

    #login登录
    # path("login/",obtain_jwt_token),
    # path("login/",token_obtain_pair),
    path("login/", login.Login.as_view()),

    # path("create/code/", code.CreateCode.as_view()),
    # code兑换码
    path(r"exchangecode/", code.CodeView.as_view()),
    re_path(r"^exchangecode/(?P<pk>\d+)/$", code.CodeView.as_view()),

]

# teacher老师
router = routers.DefaultRouter()
router.register(prefix='teacher', viewset=teacher.TeacherViewSet, basename='teacher')
print(router.urls)
urlpatterns += router.urls

# area校区
router = routers.DefaultRouter()
router.register(prefix='area', viewset=area.AreaModelViewSet, basename='area')
print(router.urls)
urlpatterns += router.urls

# school分校
router = routers.DefaultRouter()
router.register(prefix='school', viewset=school.SchoolModelViewSet, basename='school')
print(router.urls)
urlpatterns += router.urls

# batch批次
router = routers.DefaultRouter()
router.register(prefix='batch', viewset=batch.BatchModelViewSet, basename='batch')
print(router.urls)
urlpatterns += router.urls

# code兑换码
router = routers.DefaultRouter()
router.register(prefix='operate', viewset=code.CodeOperateView, basename='operate')
print(router.urls)
urlpatterns += router.urls
