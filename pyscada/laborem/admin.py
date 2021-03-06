# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from pyscada.laborem import PROTOCOL_ID
from pyscada.laborem.models import LaboremMotherboardDevice, LaboremMotherboardIOConfig, LaboremMotherboardIOElement
from pyscada.laborem.models import LaboremMotherboardVariable, LaboremPlugDevice
from pyscada.admin import DeviceAdmin
from pyscada.admin import VariableAdmin
from pyscada.admin import admin_site
from pyscada.models import Device, DeviceProtocol
from pyscada.models import Variable
from django.contrib import admin

import logging

logger = logging.getLogger(__name__)

class ExtendedLaboremMotherboardDevice(Device):
    class Meta:
        proxy = True
        verbose_name = 'Laborem Motherboard Device'
        verbose_name_plural = 'Laborem Motherboard Devices'

class LaboremMotherboardDeviceAdminInline(admin.StackedInline):
    model = LaboremMotherboardDevice

class LaboremMotherboardDeviceAdmin(DeviceAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'protocol':
            kwargs['queryset'] = DeviceProtocol.objects.filter(pk=PROTOCOL_ID)
            db_field.default = PROTOCOL_ID
        return super(LaboremMotherboardDeviceAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def get_queryset(self, request):
        """Limit Pages to those that belong to the request's user."""
        qs = super(LaboremMotherboardDeviceAdmin, self).get_queryset(request)
        return qs.filter(protocol_id=PROTOCOL_ID)

    inlines = [
        LaboremMotherboardDeviceAdminInline
    ]

class ExtendedLaboremMotherboardVariable(Variable):
    class Meta:
        proxy = True
        verbose_name = 'Laborem Motherboard Variable'
        verbose_name_plural = 'Laborem Motherboard Variables'

class LaboremMotherboardVariableAdminInline(admin.StackedInline):
    model = LaboremMotherboardVariable

class LaboremMotherboardVariableAdmin(VariableAdmin):
    list_display = ('id', 'name', 'description', 'unit', 'device_name', 'value_class', 'active', 'writeable')
    list_editable = ('active', 'writeable',)
    list_display_links = ('name',)


    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'device':
            kwargs['queryset'] = Device.objects.filter(protocol=PROTOCOL_ID)
        return super(LaboremMotherboardVariableAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def get_queryset(self, request):
        """Limit Pages to those that belong to the request's user."""
        qs = super(LaboremMotherboardVariableAdmin, self).get_queryset(request)
        return qs.filter(device__protocol_id=PROTOCOL_ID)

    inlines = [
        LaboremMotherboardVariableAdminInline
    ]

admin_site.register(ExtendedLaboremMotherboardDevice, LaboremMotherboardDeviceAdmin)
admin_site.register(ExtendedLaboremMotherboardVariable, LaboremMotherboardVariableAdmin)
admin_site.register(LaboremMotherboardIOConfig)
admin_site.register(LaboremMotherboardIOElement)
admin_site.register(LaboremPlugDevice)