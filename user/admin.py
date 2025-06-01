from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline

from .forms import ClientInteractionForm
from .models import User, UserRole, Role, Employee, ClientInteraction, Client
from django.urls import reverse
from django.utils.html import format_html


class UserRoleInline(TabularInline):
    model = UserRole
    extra = 1


class UserAdmin(ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'is_active', 'image_tag', 'edit_link', 'delete_link']
    list_display_links = ('id', 'first_name')
    list_per_page = 20
    ordering = ['id']

    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" style="object-fit: cover; border-radius: 6px;" />',
                               obj.image.url)
        return "-"

    image_tag.short_description = 'Image'

    def edit_link(self, obj):
        url = reverse('admin:%s_%s_change' % (obj._meta.app_label, obj._meta.model_name), args=[obj.id])
        return format_html(
            '<a style="background-color: blue" href="{}" class="inline-flex items-center px-2 py-1 text-sm text-white bg-yellow rounded hover:bg-yellow">'
            '<i class="fas fa-edit mr-1"></i>Edit</a>', url)

    def delete_link(self, obj):
        url = reverse('admin:%s_%s_delete' % (obj._meta.app_label, obj._meta.model_name), args=[obj.id])
        return format_html(
            '<a href="{}" class="inline-flex items-center px-2 py-1 text-sm text-white bg-red-500 rounded hover:bg-red-600">'
            '<i class="fa fa-trash mr-1"></i>Delete</a>', url)

    edit_link.short_description = 'Edit'
    edit_link.allow_tags = True

    delete_link.short_description = 'Delete'
    delete_link.allow_tags = True


admin.site.register(User, UserAdmin)


@admin.register(Role)
class RoleAdmin(ModelAdmin):
    list_display = ('role', 'description')
    search_fields = ('role', 'description')
    ordering = ('role',)


@admin.register(Employee)
class EmployeeAdmin(ModelAdmin):
    list_display = (
        'user_full_name', 'roles_display', 'start_date', 'end_date',
        'salary', 'working_hours_per_week'
    )
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'user_roles__role__role')
    list_filter = ('start_date', 'end_date', 'user_roles__role')
    ordering = ('-start_date',)

    inlines = [UserRoleInline]  # Shu yerga qo‘shiladi

    def user_full_name(self, obj):
        return obj.user.get_full_name()
    user_full_name.short_description = "Foydalanuvchi"

    def roles_display(self, obj):
        return ", ".join([ur.role.role for ur in obj.user_roles.all()])
    roles_display.short_description = "Rollar"


class ClientInteractionInline(TabularInline):
    form = ClientInteractionForm
    model = ClientInteraction
    extra = 1  # Yangi yozuv qo'shishda nechta bo'sh satr bo'lishi
    readonly_fields = ('date',)  # Yaralangan sanani o'zgartirib bo'lmasin


@admin.register(Client)
class ClientAdmin(ModelAdmin):
    list_display = ('name', 'phone', 'email', 'last_interaction_date')
    search_fields = ('name', 'phone', 'email')
    inlines = [ClientInteractionInline]

    def last_interaction_date(self, obj):
        # Mijozning eng oxirgi aloqasini topamiz
        latest = ClientInteraction.objects.filter(client=obj).order_by('-date').first()
        return latest.date if latest else "—"

    last_interaction_date.short_description = "Oxirgi aloqa"
    last_interaction_date.admin_order_field = 'date'



@admin.register(ClientInteraction)
class ClientInteractionAdmin(ModelAdmin):
    form = ClientInteractionForm
    list_display = ('client', 'date', 'subject', 'last_interaction_date')
    list_filter = ('date', 'responsible')
    search_fields = ('client__name', 'subject', 'notes')

    def last_interaction_date(self, obj):
        # Mijozning eng oxirgi aloqasini topamiz
        latest = ClientInteraction.objects.filter(client=obj.client).order_by('-date').first()
        return latest.date if latest else "—"

    last_interaction_date.short_description = "Oxirgi aloqa"
    last_interaction_date.admin_order_field = 'date'


# @admin.register(UserRole)
# class UserRoleAdmin(ModelAdmin):
#     list_display = ('employee_full_name', 'role')
#     search_fields = ('employee__user__first_name', 'employee__user__last_name', 'role__role')
#     list_filter = ('role',)
#     ordering = ('employee__user__last_name',)
#
#     def employee_full_name(self, obj):
#         return obj.employee.user.get_full_name()
#
#     employee_full_name.short_description = "Xodim"