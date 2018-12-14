#!/usr/bin/env python
# -*- coding:utf-8 -*-
# __author__ = 'Jack'

import os
import sys
import random
import django
from datetime import date

project_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_path)  # 将项目路径添加到系统搜寻路径当中
os.environ['DJANGO_SETTINGS_MODULE'] = 'imooc.settings'  # 设置项目的配置文件
django.setup()

from courses.models import Teacher, Course, Student, TeacherAssistant


def import_data():
    """使用Django ORM导入数据"""
    # 讲师数据 create()
    Teacher.objects.create(nickname="Jack", introduction="Python工程师", fans=666)
    Teacher.objects.create(nickname="Allen", introduction="Java工程师", fans=123)
    Teacher.objects.create(nickname="Henry", introduction="Golang工程师", fans=818)

    # 课程数据 bulk_create()
    Course.objects.bulk_create([Course(title=f"Python系列教程{i}", teacher=Teacher.objects.get(nickname="Jack"),
                                       type=random.choice((0, 1, 2)),
                                       price=random.randint(200, 300), volume=random.randint(100, 10000),
                                       online=date(2018, 10, 1))
                                for i in range(1, 5)])

    Course.objects.bulk_create([Course(title=f"Java系列教程{i}", teacher=Teacher.objects.get(nickname="Allen"),
                                       type=random.choice((0, 1, 2)),
                                       price=random.randint(200, 300), volume=random.randint(100, 10000),
                                       online=date(2018, 6, 4))
                                for i in range(1, 4)])

    Course.objects.bulk_create([Course(title=f"Golang系列教程{i}", teacher=Teacher.objects.get(nickname="Henry"),
                                       type=random.choice((0, 1, 2)),
                                       price=random.randint(200, 300), volume=random.randint(100, 10000),
                                       online=date(2018, 1, 1))
                                for i in range(1, 3)])

    # 学生数据 update_or_create()
    Student.objects.update_or_create(nickname="A同学", defaults={"age": random.randint(18, 58),
                                                               "gender": random.choice((0, 1, 2)),
                                                               "study_time": random.randint(9, 999)})
    Student.objects.update_or_create(nickname="B同学", defaults={"age": random.randint(18, 58),
                                                               "gender": random.choice((0, 1, 2)),
                                                               "study_time": random.randint(9, 999)})
    Student.objects.update_or_create(nickname="C同学", defaults={"age": random.randint(18, 58),
                                                               "gender": random.choice((0, 1, 2)),
                                                               "study_time": random.randint(9, 999)})
    Student.objects.update_or_create(nickname="D同学", defaults={"age": random.randint(18, 58),
                                                               "gender": random.choice((0, 1, 2)),
                                                               "study_time": random.randint(9, 999)})
    # 正向添加
    # 销量大于等于1000的课程
    Student.objects.get(nickname="A同学").course.add(*Course.objects.filter(volume__gte=1000))
    # 销量大于5000的课程
    Student.objects.get(nickname="B同学").course.add(*Course.objects.filter(volume__gt=5000))
    # 反向添加
    # 学习时间大于等于500小时的同学
    Course.objects.get(title="Python系列教程1").student_set.add(*Student.objects.filter(study_time__gte=500))
    # 学习时间小于等于500小时的同学
    Course.objects.get(title="Python系列教程2").student_set.add(*Student.objects.filter(study_time__lte=500))

    # 助教数据 get_or_create()
    TeacherAssistant.objects.get_or_create(nickname="助教1", defaults={"hobby": "慕课网学习", "teacher":
        Teacher.objects.get(nickname="Jack")})
    TeacherAssistant.objects.get_or_create(nickname="助教2", defaults={"hobby": "追慕女神", "teacher":
        Teacher.objects.get(nickname="Allen")})
    TeacherAssistant.objects.get_or_create(nickname="助教3", defaults={"hobby": "减肥减肥", "teacher":
        Teacher.objects.get(nickname="Henry")})

    return True


if __name__ == "__main__":
    if import_data():
        print("数据导入成功！")

# fixtures Django serialization → model 保存
# 数据库层面的导入数据
"""
windows下的MySQL客户端	mysql.exe/mysql -hPup 数据库名字 < 备份文件目录
						source 备份文件所在路径;
"""
# 数据库层面导出数据
"""
其它：数据库层面导出数据
		mysqldump/mysqldump.exe -hPup 数据库名字 [数据表名字1 [数据表名字2…]] > 外部文件目录(建议使用.sql)
"""
