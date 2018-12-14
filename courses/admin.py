#!/usr/bin/env python
# -*- coding:utf-8 -*-
# __author__ = 'Jack'

from django.contrib import admin
from .models import AddressInfo


class AddressAdmin(admin.ModelAdmin):
    fields = ['address', 'pid']


admin.site.register(AddressInfo, AddressAdmin)
