from django.contrib import admin
from .models import Student, Donor, RegisteredDonor, InventoryItem, Expenditure, ClassNeed, Admin


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'age', 'class_name', 'school', 'performance', 'sponsorship_status', 'sponsor')
    list_filter = ('performance', 'sponsorship_status', 'class_name')
    search_fields = ('name', 'school')


@admin.register(Donor)
class DonorAdmin(admin.ModelAdmin):
    list_display = ('name', 'donor_type', 'total_donated', 'last_donation_date')
    list_filter = ('donor_type',)
    search_fields = ('name',)


@admin.register(RegisteredDonor)
class RegisteredDonorAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'mobile_number', 'donation_frequency', 'amount_pledged')
    search_fields = ('name', 'email')


@admin.register(InventoryItem)
class InventoryItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'quantity', 'low_stock_threshold', 'is_low_stock')
    list_filter = ('category',)
    search_fields = ('name',)


@admin.register(Expenditure)
class ExpenditureAdmin(admin.ModelAdmin):
    list_display = ('description', 'amount', 'date', 'category')
    list_filter = ('category', 'date')
    search_fields = ('description',)


@admin.register(ClassNeed)
class ClassNeedAdmin(admin.ModelAdmin):
    list_display = ('class_name', 'item', 'quantity_needed', 'cost_per_item', 'total')
    list_filter = ('class_name',)


@admin.register(Admin)
class AdminAdmin(admin.ModelAdmin):
    list_display = ('email', 'name', 'created_at')
    search_fields = ('email', 'name')

