from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('home/', views.home, name='home'),
    
    # Admin routes
    path('admin-login/', views.admin_login, name='admin_login'),
    path('admin-forgot-password/', views.admin_forgot_password, name='admin_forgot_password'),
    path('admin-verify-security/', views.admin_verify_security, name='admin_verify_security'),
    path('admin-reset-password/', views.admin_reset_password, name='admin_reset_password'),
    path('admin/logout/', views.admin_logout, name='admin_logout'),
    path('admin/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/students/', views.admin_students, name='admin_students'),
    path('admin/students/create/', views.student_create, name='student_create'),
    path('admin/students/<int:student_id>/edit/', views.student_edit, name='student_edit'),
    path('admin/students/<int:student_id>/delete/', views.student_delete, name='student_delete'),
    path('admin/donors/', views.admin_donors, name='admin_donors'),
    path('admin/donors/<int:donor_id>/record-donation/', views.admin_record_donation, name='admin_record_donation'),
    path('admin/donors/<int:donor_id>/reject-donation/', views.admin_reject_donation, name='admin_reject_donation'),
    path('admin/inventory/', views.admin_inventory, name='admin_inventory'),
    path('admin/inventory/create/', views.inventory_create, name='inventory_create'),
    path('admin/inventory/<int:item_id>/edit/', views.inventory_edit, name='inventory_edit'),
    path('admin/inventory/<int:item_id>/update-stock/', views.inventory_update_stock, name='inventory_update_stock'),
    path('admin/inventory/<int:item_id>/delete/', views.inventory_delete, name='inventory_delete'),
    path('admin/finances/', views.admin_finances, name='admin_finances'),
    path('admin/finances/expenditures/create/', views.expenditure_create, name='expenditure_create'),
    path('admin/finances/expenditures/<int:expenditure_id>/edit/', views.expenditure_edit, name='expenditure_edit'),
    path('admin/finances/expenditures/<int:expenditure_id>/delete/', views.expenditure_delete, name='expenditure_delete'),
    path('admin/finances/classneeds/create/', views.classneed_create, name='classneed_create'),
    path('admin/finances/classneeds/<int:classneed_id>/edit/', views.classneed_edit, name='classneed_edit'),
    path('admin/finances/classneeds/<int:classneed_id>/delete/', views.classneed_delete, name='classneed_delete'),
    
    # Donor routes
    path('donate/', views.donate, name='donate'),
    path('register-donor/', views.donor_registration, name='donor_registration'),
    path('donor-login/', views.donor_login, name='donor_login'),
    path('donor-forgot-password/', views.donor_forgot_password, name='donor_forgot_password'),
    path('donor-verify-security/', views.donor_verify_security, name='donor_verify_security'),
    path('donor-reset-password/', views.donor_reset_password, name='donor_reset_password'),
    path('donor/logout/', views.donor_logout, name='donor_logout'),
    path('donor-dashboard/', views.donor_dashboard, name='donor_dashboard'),
    path('donor/update-donation/', views.donor_update_donation, name='donor_update_donation'),
    path('donor/remove-donation/', views.donor_remove_donation, name='donor_remove_donation'),
    path('donor/edit-profile/', views.donor_edit_profile, name='donor_edit_profile'),
    
    # Session check
    path('check-session/', views.check_session, name='check_session'),
]

