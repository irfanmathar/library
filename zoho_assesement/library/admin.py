from django.contrib import admin
from .models import *
from django.contrib.auth.models import User, Group

class BookAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        if obj.status == 'Returned':
            obj.book.available_copies += 1
        elif obj.status == 'Issued':
            obj.book.available_copies -= 1
        obj.book.save()
        super().save_model(request, obj, form, change)

admin.site.register(Books, BookAdmin)
admin.site.register(Members)
admin.site.register(Transactions)
admin.site.register(Staffs)
