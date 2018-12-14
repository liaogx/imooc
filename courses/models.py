#!/usr/bin/env python
# -*- coding:utf-8 -*-
# __author__ = "Jack"


from django.db import models

# class Test(models.Model):  # courses_test
#     """测试学习用"""
#     # Auto = models.AutoField()  # 自增长字段
#     # BigAuto = models.BigAutoField()
#
#     # 二进制数据
#     Binary = models.BinaryField()
#
#     # 布尔型
#     Boolean = models.BooleanField()
#     NullBoolean = models.NullBooleanField()
#
#     # 整型
#     PositiveSmallInteger = models.PositiveSmallIntegerField(db_column="age")  # 5个字节
#     SmallInteger = models.SmallIntegerField(primary_key=False)  # 6个字节
#     PositiveInteger = models.PositiveIntegerField()  # 10个字节
#     Integer = models.IntegerField(verbose_name="11个字节大小")  # 11个字节
#     BigInteger = models.BigIntegerField(unique=True)  # 20个字节
#
#     # 字符串类型
#     Char = models.CharField(max_length=100, null=True, blank=True, db_index=True)  # varchar
#     Text = models.TextField(help_text="这个是longtext")  # longtext
#
#     # 时间日期类型
#     Date = models.DateField(unique_for_date=True, auto_now=True)
#     DateTime = models.DateTimeField(editable=False, unique_for_month=True, auto_now_add=True)
#     Duration = models.DurationField()  # int, Python timedelta实现
#
#     # 浮点型
#     Float = models.FloatField()
#     Decimal = models.DecimalField(max_digits=4, decimal_places=2)  # 11.22, 16.34
#
#     # 其它字段
#     Email = models.EmailField()  # 邮箱
#     Image = models.ImageField()
#     File = models.FileField()
#     FilePath = models.FilePathField()
#     URL = models.URLField()
#     UUID = models.UUIDField()
#     GenericIPAddress = models.GenericIPAddressField()
#
#
# class A(models.Model):
#     onetoone = models.OneToOneField(Test, related_name="one")
#
#
# class B(models.Model):
#     foreign = models.ForeignKey(A, on_delete=models.CASCADE)  # 删除级联
#     # foreign = models.ForeignKey(A, on_delete=models.PROTECT)
#     # foreign = models.ForeignKey(A, on_delete=models.SET_NULL, null=True, blank=True)  # 删除置空
#     # foreign = models.ForeignKey(A, on_delete=models.SET_DEFAULT, default=0)
#     # foreign = models.ForeignKey(A, on_delete=models.DO_NOTHING)
#     # foreign = models.ForeignKey(A, on_delete=models.SET)
#
#
# class C(models.Model):
#     manytomany = models.ManyToManyField(B)


# 1.所有字段都有的参数
# 2.个别字段才有的参数
# 3.关系型字段的参数

"""
on_delete 当一个被外键关联的对象被删除时，Django将模仿on_delete参数定义的SQL约束执行相应操作
	如下6种操作
	CASCADE：模拟SQL语言中的ON DELETE CASCADE约束，将定义有外键的模型对象同时删除！（该操作为当前Django版本的默认操作！）
	PROTECT:阻止上面的删除操作，但是弹出ProtectedError异常
	SET_NULL：将外键字段设为null，只有当字段设置了null=True时，方可使用该值。
	SET_DEFAULT:将外键字段设为默认值。只有当字段设置了default参数时，方可使用。
	DO_NOTHING：什么也不做。
	SET()：设置为一个传递给SET()的值或者一个回调函数的返回值。注意大小写。
"""


class AddressInfo(models.Model):  # coures_addressinfo
    """省市县地址信息"""
    address = models.CharField(max_length=200, null=True, blank=True, verbose_name="地址")
    pid = models.ForeignKey('self', null=True, blank=True, verbose_name="自关联")
    # pid = models.ForeignKey('AddressInfo', null=True, blank=True, verbose_name="自关联")
    note = models.CharField(max_length=200, null=True, blank=True, verbose_name="说明")

    def __str__(self):  # __unicode__(self)
        return self.address

    class Meta:
        # 定义元数据
        db_table = 'address'
        # ordering = ['pid']  # 指定按照什么字段排序
        verbose_name = '省市县地址信息'
        verbose_name_plural = verbose_name
        # abstract = True
        # permissions = (('定义好的权限', '权限说明'),)
        # managed = False
        unique_together = ('address', 'note')  # ((),())
        # app_label = 'courses'
        # db_tablespace  # 定义数据库表空间的名字


class Teacher(models.Model):
    """讲师信息表"""
    nickname = models.CharField(max_length=30, primary_key=True, db_index=True, verbose_name="昵称")
    introduction = models.TextField(default="这位同学很懒，木有签名的说~", verbose_name="简介")
    fans = models.PositiveIntegerField(default="0", verbose_name="粉丝数")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        verbose_name = "讲师信息表"
        verbose_name_plural = verbose_name

    def __str__(self):  # Python2:__unicode__
        return self.nickname


class Course(models.Model):
    """课程信息表"""
    title = models.CharField(max_length=100, primary_key=True, db_index=True, verbose_name="课程名")
    teacher = models.ForeignKey(Teacher, null=True, blank=True, on_delete=models.CASCADE,
                                verbose_name="课程讲师")  # 删除级联
    type = models.CharField(choices=((1, "实战课"), (2, "免费课"), (0, "其它")), max_length=1,
                            default=0, verbose_name="课程类型")
    price = models.PositiveSmallIntegerField(verbose_name="价格")
    volume = models.BigIntegerField(verbose_name="销量")
    online = models.DateField(verbose_name="上线时间")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        verbose_name = "课程信息表"
        get_latest_by = "created_at"
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.get_type_display()}-{self.title}"  # 示例：实战课-Django零基础入门到实战
        # return "{}-{}".format(self.get_type_display(), self.title)  # 示例：实战课-Django零基础入门到实战


class Student(models.Model):
    """学生信息表"""
    nickname = models.CharField(max_length=30, primary_key=True, db_index=True, verbose_name="昵称")
    course = models.ManyToManyField(Course, verbose_name="课程")
    age = models.PositiveSmallIntegerField(verbose_name="年龄")
    gender = models.CharField(choices=((1, "男"), (2, "女"), (0, "保密")), max_length=1,
                              default=0, verbose_name="性别")
    study_time = models.PositiveIntegerField(default="0", verbose_name="学习时长(h)")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        verbose_name = "学生信息表"
        ordering = ['age']
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.nickname


class TeacherAssistant(models.Model):
    """助教信息表"""
    nickname = models.CharField(max_length=30, primary_key=True, db_index=True, verbose_name="昵称")
    teacher = models.OneToOneField(Teacher, null=True, blank=True, on_delete=models.SET_NULL,
                                   verbose_name="讲师")  # 删除置空
    hobby = models.CharField(max_length=100, null=True, blank=True, verbose_name="爱好")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        verbose_name = "助教信息表"
        db_table = "courses_assistant"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.nickname


class GroupConcat(models.Aggregate):
    """自定义实现聚合功能，实现GROUP_CONCAT功能"""

    function = 'GROUP_CONCAT'
    template = '%(function)s(%(distinct)s%(expressions)s%(ordering)s%(separator)s)'

    def __init__(self, expression, distinct=False, ordering=None, separator=',', **extra):
        super(GroupConcat, self).__init__(expression,
                                          distinct='DISTINCT ' if distinct else '',
                                          ordering=' ORDER BY %s' % ordering if ordering is not None else '',
                                          separator=' SEPARATOR "%s"' % separator,
                                          output_field=models.CharField(), **extra)
