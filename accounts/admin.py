from django.contrib import admin

from accounts.models import Customer, Order, Product, Tag


class CustomerAdminForm(admin.ModelAdmin):
    list_display = ['name','phone','email','date_created']

    search_fields = ['name','email']

    list_display_links = ['name','email','phone']

    ordering = ['id']

    list_filter = ['date_created']




admin.site.register(Customer,CustomerAdminForm)
admin.site.register(Order)
admin.site.register(Product)
admin.site.register(Tag)
admin.site.site_title = "Dennis Ivy Project"