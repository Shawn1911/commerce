from django.contrib import admin

from .models import (Person, Plan, PlanInvoice, PlanPricing, PlanQuotas,
                     Quotas, ShopUser, User,)


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone')
    search_fields = ('name', 'phone')


@admin.register(ShopUser)
class ShopUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'type', 'last_activity', 'is_blocked', 'language', 'shop')
    search_fields = ('username', 'email', 'telegram_id')
    list_filter = ('type', 'is_blocked', 'is_active', 'is_staff')
    readonly_fields = ('last_activity',)
    ordering = ('-last_activity',)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'type', 'is_active', 'language', 'default_shop')
    search_fields = ('username', 'email', 'invitation_code')
    list_filter = ('type', 'is_active', 'is_staff')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)


@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'description')
    search_fields = ('name', 'code')


@admin.register(PlanPricing)
class PlanPricingAdmin(admin.ModelAdmin):
    list_display = ('name', 'period_type', 'currency', 'price', 'original_price', 'period', 'plan')
    search_fields = ('name', 'plan__name')
    list_filter = ('period_type', 'currency')


@admin.register(Quotas)
class QuotasAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)


@admin.register(PlanQuotas)
class PlanQuotasAdmin(admin.ModelAdmin):
    list_display = ('plan', 'quotas', 'value')
    search_fields = ('plan__name', 'quotas__name')


@admin.register(PlanInvoice)
class PlanInvoiceAdmin(admin.ModelAdmin):
    list_display = ('user', 'plan', 'price', 'status', 'payed_at', 'plan_extended_from', 'plan_extended_until')
    search_fields = ('user__email', 'plan__name', 'price')
    list_filter = ('status',)
    date_hierarchy = 'payed_at'
    readonly_fields = ('payed_at',)
