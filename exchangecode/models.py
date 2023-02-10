import time

from django.db import models


# Create your models here.
from django.utils.timezone import localdate, now

from django.contrib.auth.models import AbstractUser

class Area(models.Model):
    area_name = models.CharField(max_length=64,unique=True, verbose_name="区域名称")

    def __str__(self):
        return self.area_name


class School(models.Model):
    school_name = models.CharField(max_length=64,unique=True, verbose_name="分校名称")
    area = models.ForeignKey(to=Area, on_delete=models.SET(0),verbose_name="所属区域id")

    def __str__(self):
        return self.school_name

class Teacher(AbstractUser):
    phone_num = models.CharField(max_length=11, unique=True, verbose_name="手机号")
    # 这里area和school都没有给默认值，是因为有valiadate函数需要校验正确性，给了默认值在serializers就不是必填项了
    area = models.ForeignKey(to=Area,on_delete=models.SET(1),verbose_name="所属区域")
    school = models.ForeignKey(to=School,on_delete=models.SET(1),verbose_name="所属分校")


class Batch(models.Model):
    class status(models.IntegerChoices):
        NORMAL=1,"正常"
        EXPIRE=2,"已过期"

    def get_expire_status(self):
        if self.expire_time<now().date():
            return self.status.EXPIRE.label
        else:
            return self.status.NORMAL.label

    def get_area_name(self):
        area_name=Area.objects.all().get(pk=self.area_id)
        if area_name:
            return area_name
        else:
            return "未知校区"

    batch_name = models.CharField(max_length=64,unique=True, verbose_name="批次名称")
    expire_time = models.DateField(verbose_name="过期时间")
    area_id = models.IntegerField(verbose_name="所属区域")
    exchange_link = models.CharField(max_length=255, verbose_name="兑换链接")
    create_user=models.CharField(max_length=64,null=True,verbose_name="创建人")
    create_time= models.DateTimeField(null=True,verbose_name="创建时间")
    
    class Meta:
        ordering = ('-expire_time',)

class Code(models.Model):
    class status_emun(models.IntegerChoices):
        FREE=1,"空闲"
        USED=2,"已使用"

    def get_school_name(self):
        if not self.school_id:
            return ""
        school_name = School.objects.all().filter(pk=self.school_id).first().school_name
        if school_name:
            return school_name
        else:
            return "未知分校"

    code_name= models.CharField(max_length=64,unique=True, verbose_name="兑换码")
    batch=models.ForeignKey(to=Batch,on_delete=models.CASCADE,verbose_name="批次号")
    school_id = models.IntegerField(null=True,verbose_name="所属分校")
    status=models.IntegerField(choices=status_emun.choices,default=status_emun.FREE,verbose_name="使用状态:1空闲,2已使用(默认为0)")
    student_name=models.CharField(max_length=64, null=True,verbose_name="学生姓名")
    student_grade=models.CharField(max_length=10, null=True,verbose_name="学生年级")
    student_major=models.CharField(max_length=10, null=True,verbose_name="学生专业")
    operator_user=models.CharField(max_length=64,null=True,verbose_name="操作人")
    operator_time= models.DateTimeField(null=True,verbose_name="操作时间")



