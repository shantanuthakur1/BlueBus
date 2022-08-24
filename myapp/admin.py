from django.contrib import admin
from .models import Bus, User, Book, Route
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm
# Register your models here.

class CustomUserAdmin(UserAdmin):
    model = User
    add_form = CustomUserCreationForm
    fieldsets = (
        *UserAdmin.fieldsets,
        (
            'User Info',
            {
                'fields': (
                    'email_id',
                    'name'
                )
            }
        )
    )



admin.site.register(Bus)
admin.site.register(User, CustomUserAdmin)
admin.site.register(Book)
admin.site.register(Route)


