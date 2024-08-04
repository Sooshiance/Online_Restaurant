from django.contrib import admin

from vendor.models import  Vendor


class VendorAdmin(admin.ModelAdmin):
    list_display = ('user', 'vendor_name', 'is_approved')
    list_filter = ['is_approved']


admin.site.register(Vendor, VendorAdmin)
