from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Sum, Count, F
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from datetime import datetime, timedelta
from decimal import Decimal, InvalidOperation
from .models import Student, Donor, RegisteredDonor, InventoryItem, Expenditure, ClassNeed


def get_available_funds():
    total_donations = Donor.objects.aggregate(Sum('total_donated'))['total_donated__sum'] or Decimal('0')
    total_expenditures = Expenditure.objects.aggregate(Sum('amount'))['amount__sum'] or Decimal('0')
    return Decimal(str(total_donations)) - Decimal(str(total_expenditures))


def home(request):
    from datetime import datetime
    from .models import Admin, RegisteredDonor
    
    available_funds = get_available_funds()
    funds_low = available_funds < Decimal('50000')
    
    admin_authenticated = request.session.get('admin_authenticated', False)
    admin_name = None
    admin_email = None
    if admin_authenticated:
        admin_email = request.session.get('admin_email')
        admin_id = request.session.get('admin_id')
        if admin_id:
            try:
                admin = Admin.objects.get(id=admin_id)
                admin_name = admin.name
            except Admin.DoesNotExist:
                pass
        if not admin_name and admin_email:
            admin_name = admin_email.split('@')[0]
    
    donor_authenticated = request.session.get('donor_authenticated', False)
    donor_name = None
    if donor_authenticated:
        donor_id = request.session.get('donor_id')
        if donor_id:
            try:
                donor = RegisteredDonor.objects.get(id=donor_id)
                donor_name = donor.name
            except RegisteredDonor.DoesNotExist:
                pass
    
    return render(request, 'core/home.html', {
        'current_year': datetime.now().year,
        'available_funds': available_funds,
        'funds_low': funds_low,
        'admin_authenticated': admin_authenticated,
        'admin_name': admin_name,
        'donor_authenticated': donor_authenticated,
        'donor_name': donor_name,
    })


@require_http_methods(["GET", "POST"])
def admin_login(request):
    from datetime import datetime
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        if not email or not password:
            messages.error(request, 'Please provide both email and password.')
        else:
            from .models import Admin
            try:
                admin = Admin.objects.get(email=email)
                if admin.check_password(password):
                    request.session['admin_authenticated'] = True
                    request.session['admin_id'] = admin.id
                    request.session['admin_email'] = admin.email
                    request.session['last_activity'] = datetime.now().isoformat()
                    return redirect('admin_dashboard')
                else:
                    messages.error(request, 'Invalid email or password. Please try again.')
            except Admin.DoesNotExist:
                messages.error(request, 'Invalid email or password. Please try again.')
            except Exception as e:
                messages.error(request, 'Unable to process your request. Please check your credentials and try again.')
    
    return render(request, 'core/admin_login.html', {
        'current_year': datetime.now().year
    })


def admin_logout(request):
    request.session.pop('admin_authenticated', None)
    request.session.pop('admin_id', None)
    request.session.pop('admin_email', None)
    request.session.pop('last_activity', None)
    messages.success(request, 'You have been successfully logged out.')
    return redirect('home')


@require_http_methods(["GET", "POST"])
def admin_forgot_password(request):
    from datetime import datetime
    from .models import Admin
    
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        
        if not email:
            messages.error(request, 'Please enter your email address.')
        else:
            try:
                admin = Admin.objects.get(email=email)
                
                request.session['password_reset_user_type'] = 'admin'
                request.session['password_reset_user_id'] = admin.id
                request.session['password_reset_email'] = email
                request.session['password_reset_attempts'] = 0
                
                return redirect('admin_verify_security')
            except Admin.DoesNotExist:
                messages.error(request, 'If an account exists with this email, you will be shown a security question.')
            except Exception as e:
                messages.error(request, 'An error occurred. Please try again.')
    
    return render(request, 'core/admin_forgot_password.html', {
        'current_year': datetime.now().year
    })


@require_http_methods(["GET", "POST"])
def admin_verify_security(request):
    from datetime import datetime
    from .models import Admin
    
    if request.session.get('password_reset_user_type') != 'admin':
        messages.error(request, 'Please request a password reset first.')
        return redirect('admin_forgot_password')
    
    admin_id = request.session.get('password_reset_user_id')
    if not admin_id:
        messages.error(request, 'Session expired. Please start again.')
        return redirect('admin_forgot_password')
    
    try:
        admin = Admin.objects.get(id=admin_id)
    except Admin.DoesNotExist:
        messages.error(request, 'Account not found. Please try again.')
        request.session.pop('password_reset_user_type', None)
        request.session.pop('password_reset_user_id', None)
        request.session.pop('password_reset_email', None)
        return redirect('admin_forgot_password')
    
    attempts = request.session.get('password_reset_attempts', 0)
    
    if attempts >= 3:
        messages.error(request, 'Maximum attempts exceeded. Please contact support.')
        request.session.pop('password_reset_user_type', None)
        request.session.pop('password_reset_user_id', None)
        request.session.pop('password_reset_email', None)
        request.session.pop('password_reset_attempts', None)
        return redirect('admin_forgot_password')
    
    if request.method == 'POST':
        security_answer = request.POST.get('security_answer', '').strip().lower()
        
        if not security_answer:
            messages.error(request, 'Please enter your security answer.')
        else:
            if security_answer == admin.security_answer.lower().strip():
                request.session['password_reset_verified'] = True
                request.session.pop('password_reset_attempts', None)
                messages.success(request, 'Security answer verified. Please set your new password.')
                return redirect('admin_reset_password')
            else:
                request.session['password_reset_attempts'] = attempts + 1
                remaining = 3 - (attempts + 1)
                if remaining > 0:
                    messages.error(request, f'Incorrect security answer. {remaining} attempt(s) remaining.')
                else:
                    messages.error(request, 'Maximum attempts exceeded. Please contact support.')
                    request.session.pop('password_reset_user_type', None)
                    request.session.pop('password_reset_user_id', None)
                    request.session.pop('password_reset_email', None)
                    request.session.pop('password_reset_attempts', None)
                    return redirect('admin_forgot_password')
    
    return render(request, 'core/admin_verify_security.html', {
        'current_year': datetime.now().year,
        'security_question': admin.security_question,
        'remaining_attempts': 3 - attempts
    })


@require_http_methods(["GET", "POST"])
def admin_reset_password(request):
    from datetime import datetime
    import re
    from .models import Admin
    
    if not request.session.get('password_reset_verified'):
        messages.error(request, 'Please verify your OTP first.')
        return redirect('admin_forgot_password')
    
    if request.session.get('password_reset_user_type') != 'admin':
        messages.error(request, 'Invalid session. Please start again.')
        return redirect('admin_forgot_password')
    
    admin_id = request.session.get('password_reset_user_id')
    
    if not admin_id:
        messages.error(request, 'Session expired. Please start again.')
        return redirect('admin_forgot_password')
    
    try:
        admin = Admin.objects.get(id=admin_id)
    except Admin.DoesNotExist:
        messages.error(request, 'Account not found. Please try again.')
        request.session.pop('password_reset_verified', None)
        request.session.pop('password_reset_email', None)
        request.session.pop('password_reset_user_type', None)
        request.session.pop('password_reset_user_id', None)
        return redirect('admin_forgot_password')
    
    if request.method == 'POST':
        new_password = request.POST.get('new_password', '').strip()
        confirm_password = request.POST.get('confirm_password', '').strip()
        
        if not new_password:
            messages.error(request, 'Please enter a new password.')
        elif not confirm_password:
            messages.error(request, 'Please confirm your new password.')
        elif new_password != confirm_password:
            messages.error(request, 'Passwords do not match. Please try again.')
        else:
            # Password validation: minimum 6 characters, one capital, one small, one special character, one number
            password_errors = []
            if len(new_password) < 6:
                password_errors.append('Password must be at least 6 characters long.')
            if not re.search(r'[A-Z]', new_password):
                password_errors.append('Password must contain at least one capital letter.')
            if not re.search(r'[a-z]', new_password):
                password_errors.append('Password must contain at least one small letter.')
            if not re.search(r'[0-9]', new_password):
                password_errors.append('Password must contain at least one number.')
            if not re.search(r'[!@#$%^&*()_+\-=\[\]{};\':"\\|,.<>\/?]', new_password):
                password_errors.append('Password must contain at least one special character (!@#$%^&* etc.).')
            
            if password_errors:
                messages.error(request, 'Password validation failed: ' + ' '.join(password_errors))
            else:
                admin.set_password(new_password)
                admin.save()
                
                # Clear all password reset session data
                request.session.pop('password_reset_verified', None)
                request.session.pop('password_reset_mobile', None)
                request.session.pop('password_reset_user_type', None)
                request.session.pop('password_reset_user_id', None)
                request.session.pop('password_reset_last_request', None)
                
                messages.success(request, 'Password reset successfully! Please login with your new password.')
                return redirect('admin_login')
    
    return render(request, 'core/admin_reset_password.html', {
        'current_year': datetime.now().year,
        'admin': admin
    })


def check_session(request):
    """Check if user session is still valid and update last activity"""
    from datetime import datetime, timedelta
    
    admin_authenticated = request.session.get('admin_authenticated', False)
    donor_authenticated = request.session.get('donor_authenticated', False)
    
    # Track user type before clearing (for redirect purposes)
    user_type = None
    if admin_authenticated:
        user_type = 'admin'
    elif donor_authenticated:
        user_type = 'donor'
    
    # Check if session has expired (Django will automatically expire sessions)
    # Also check inactivity timeout (1 hour)
    is_valid = False
    if admin_authenticated or donor_authenticated:
        last_activity_str = request.session.get('last_activity')
        if last_activity_str:
            try:
                last_activity = datetime.fromisoformat(last_activity_str)
                time_since_activity = datetime.now() - last_activity
                # Check if more than 1 hour of inactivity
                if time_since_activity < timedelta(hours=1):
                    is_valid = True
                    # Update last activity
                    request.session['last_activity'] = datetime.now().isoformat()
                else:
                    # Session expired due to inactivity, clear session
                    request.session.pop('admin_authenticated', None)
                    request.session.pop('admin_id', None)
                    request.session.pop('admin_email', None)
                    request.session.pop('donor_authenticated', None)
                    request.session.pop('donor_id', None)
                    request.session.pop('last_activity', None)
                    admin_authenticated = False
                    donor_authenticated = False
            except (ValueError, TypeError):
                # Invalid timestamp, consider expired
                is_valid = False
        else:
            # No last_activity recorded, but session exists - set it now
            request.session['last_activity'] = datetime.now().isoformat()
            is_valid = True
    
    return JsonResponse({
        'valid': is_valid,
        'admin_authenticated': admin_authenticated,
        'donor_authenticated': donor_authenticated,
        'user_type': user_type  # Return user type even after expiry
    })


def admin_required(view_func):
    """Decorator to check admin authentication and add admin context"""
    def wrapper(request, *args, **kwargs):
        if not request.session.get('admin_authenticated'):
            return redirect('admin_login')
        
        # Add admin name to request for use in templates
        from .models import Admin
        admin_name = None
        admin_id = request.session.get('admin_id')
        admin_email = request.session.get('admin_email')
        
        if admin_id:
            try:
                admin = Admin.objects.get(id=admin_id)
                admin_name = admin.name
            except Admin.DoesNotExist:
                pass
        
        if not admin_name and admin_email:
            admin_name = admin_email.split('@')[0]
        
        # Store in request for template access
        request.admin_name = admin_name
        
        # Get response from view
        response = view_func(request, *args, **kwargs)
        
        # Add admin_name and admin_authenticated to context for TemplateResponse
        from django.template.response import TemplateResponse
        if isinstance(response, TemplateResponse):
            if response.context_data is None:
                response.context_data = {}
            response.context_data['admin_name'] = admin_name
            response.context_data['admin_authenticated'] = True
        
        return response
    return wrapper


@admin_required
def admin_dashboard(request):
    """Admin dashboard view"""
    total_students = Student.objects.count()
    sponsored_students = Student.objects.filter(sponsorship_status='Sponsored').count()
    unsponsored_students = total_students - sponsored_students
    total_donors = Donor.objects.count()
    total_donations = Donor.objects.aggregate(Sum('total_donated'))['total_donated__sum'] or Decimal('0')
    total_expenditures = Expenditure.objects.aggregate(Sum('amount'))['amount__sum'] or Decimal('0')
    available_funds = get_available_funds()
    low_stock_items = InventoryItem.objects.filter(quantity__lte=F('low_stock_threshold')).count()
    recent_expenditures = Expenditure.objects.all()[:5]
    class_needs = ClassNeed.objects.all()
    
    return render(request, 'core/admin/dashboard.html', {
        'total_students': total_students,
        'sponsored_students': sponsored_students,
        'unsponsored_students': unsponsored_students,
        'total_donors': total_donors,
        'total_donations': total_donations,
        'total_expenditures': total_expenditures,
        'available_funds': available_funds,
        'low_stock_items': low_stock_items,
        'recent_expenditures': recent_expenditures,
        'class_needs': class_needs,
    })


@admin_required
def admin_students(request):
    """Students management view"""
    students = Student.objects.all()
    return render(request, 'core/admin/students.html', {
        'students': students
    })


@admin_required
@require_http_methods(["GET", "POST"])
def student_create(request):
    """Create new student"""
    if request.method == 'POST':
        try:
            student = Student.objects.create(
                name=request.POST.get('name'),
                age=int(request.POST.get('age')),
                class_name=request.POST.get('class_name'),
                school=request.POST.get('school'),
                parental_income=float(request.POST.get('parental_income', 0)),
                help_provided=request.POST.get('help_provided', ''),
                performance=request.POST.get('performance', 'Average'),
                sponsorship_status=request.POST.get('sponsorship_status', 'Not Sponsored'),
                gender=request.POST.get('gender', '')
            )
            messages.success(request, f'Student "{student.name}" has been successfully added!')
            return redirect('admin_students')
        except ValueError as e:
            messages.error(request, 'Please check your input. Age and income must be valid numbers.')
        except Exception as e:
            messages.error(request, 'Unable to create student. Please verify all required fields are filled correctly.')
    
    return render(request, 'core/admin/student_form.html', {
        'action': 'Create'
    })


@admin_required
@require_http_methods(["GET", "POST"])
def student_edit(request, student_id):
    """Edit student"""
    student = get_object_or_404(Student, id=student_id)
    
    if request.method == 'POST':
        try:
            student.name = request.POST.get('name')
            student.age = int(request.POST.get('age'))
            student.class_name = request.POST.get('class_name')
            student.school = request.POST.get('school')
            student.parental_income = float(request.POST.get('parental_income', 0))
            student.help_provided = request.POST.get('help_provided', '')
            student.performance = request.POST.get('performance', 'Average')
            student.sponsorship_status = request.POST.get('sponsorship_status', 'Not Sponsored')
            student.gender = request.POST.get('gender', '')
            student.save()
            messages.success(request, f'Student "{student.name}" has been successfully updated!')
            return redirect('admin_students')
        except ValueError as e:
            messages.error(request, 'Please check your input. Age and income must be valid numbers.')
        except Exception as e:
            messages.error(request, 'Unable to update student. Please verify all required fields are filled correctly.')
    
    return render(request, 'core/admin/student_form.html', {
        'student': student,
        'action': 'Edit'
    })


@admin_required
def student_delete(request, student_id):
    """Delete student"""
    student = get_object_or_404(Student, id=student_id)
    if request.method == 'POST':
        student_name = student.name
        student.delete()
        messages.success(request, f'Student "{student_name}" has been successfully removed from the system.')
        return redirect('admin_students')
    return render(request, 'core/admin/student_confirm_delete.html', {'student': student})


@admin_required
def admin_donors(request):
    """Donors management view"""
    donors = Donor.objects.all().order_by('-last_donation_date', '-total_donated')
    # Only show registered donors who still have a desired donation (ready to contact)
    registered_donors_ready = RegisteredDonor.objects.filter(desired_donation__gt=0).order_by('-desired_donation', '-created_at')
    # All registered donors (for stats)
    all_registered_donors = RegisteredDonor.objects.all()
    total_donations = donors.aggregate(Sum('total_donated'))['total_donated__sum'] or 0
    total_registered_donations = all_registered_donors.aggregate(Sum('total_donated'))['total_donated__sum'] or 0
    return render(request, 'core/admin/donors.html', {
        'donors': donors,
        'registered_donors': registered_donors_ready,
        'total_donations': total_donations,
        'total_registered_donations': total_registered_donations
    })


@admin_required
@require_http_methods(["GET", "POST"])
def admin_record_donation(request, donor_id):
    """Record a donation received from a registered donor"""
    donor = get_object_or_404(RegisteredDonor, id=donor_id)
    
    if request.method == 'POST':
        try:
            from datetime import date
            from decimal import Decimal
            
            donation_amount = Decimal(request.POST.get('donation_amount', 0))
            use_desired_amount = request.POST.get('use_desired_amount') == 'on'
            
            if use_desired_amount and donor.desired_donation > 0:
                donation_amount = Decimal(str(donor.desired_donation))
            
            if donation_amount <= 0:
                messages.error(request, 'Donation amount must be greater than zero.')
            else:
                # Update donor's total donated (convert to Decimal for proper addition)
                donor.total_donated = Decimal(str(donor.total_donated)) + donation_amount
                donor.last_donation_date = date.today()
                
                # If using desired amount, reset it after recording
                if use_desired_amount:
                    donor.desired_donation = Decimal('0')
                else:
                    # If partial donation, reduce desired amount
                    current_desired = Decimal(str(donor.desired_donation))
                    if donation_amount <= current_desired:
                        donor.desired_donation = current_desired - donation_amount
                    else:
                        # If more than desired, set to 0
                        donor.desired_donation = Decimal('0')
                
                donor.save()
                
                # Update or create a Donor record for historical tracking
                # Check if a Donor record already exists for this person
                existing_donor, created = Donor.objects.get_or_create(
                    name=donor.name,
                    defaults={
                        'donor_type': 'Individual',
                        'total_donated': donation_amount,
                        'last_donation_date': date.today()
                    }
                )
                
                if not created:
                    # Update existing donor record (Donor model also uses DecimalField)
                    existing_total = Decimal(str(existing_donor.total_donated))
                    existing_donor.total_donated = existing_total + donation_amount
                    existing_donor.last_donation_date = date.today()
                    existing_donor.save()
                
                messages.success(request, f'Donation of ₹{float(donation_amount):.2f} from {donor.name} has been successfully recorded!')
                return redirect('admin_donors')
        except ValueError:
            messages.error(request, 'Please enter a valid donation amount.')
        except Exception as e:
            messages.error(request, f'Error recording donation: {str(e)}')
    
    return render(request, 'core/admin/record_donation.html', {'donor': donor})


@admin_required
@require_http_methods(["POST"])
def admin_reject_donation(request, donor_id):
    """Reject a donation request by setting desired_donation to 0"""
    donor = get_object_or_404(RegisteredDonor, id=donor_id)
    try:
        from decimal import Decimal
        donor.desired_donation = Decimal('0')
        donor.save()
        messages.success(request, f'Donation request from {donor.name} has been rejected. The donor has been removed from the contact list.')
    except Exception as e:
        messages.error(request, 'Unable to reject donation. Please try again.')
    
    return redirect('admin_donors')


@admin_required
def admin_inventory(request):
    """Inventory management view"""
    inventory = InventoryItem.objects.all()
    return render(request, 'core/admin/inventory.html', {
        'inventory': inventory
    })


@admin_required
@require_http_methods(["GET", "POST"])
def inventory_create(request):
    """Create new inventory item"""
    if request.method == 'POST':
        try:
            item = InventoryItem.objects.create(
                name=request.POST.get('name'),
                category=request.POST.get('category'),
                quantity=int(request.POST.get('quantity', 0)),
                low_stock_threshold=int(request.POST.get('low_stock_threshold', 10))
            )
            messages.success(request, f'Inventory item "{item.name}" has been successfully added!')
            return redirect('admin_inventory')
        except ValueError as e:
            messages.error(request, 'Please check your input. Quantity and threshold must be valid numbers.')
        except Exception as e:
            messages.error(request, 'Unable to create inventory item. Please verify all required fields are filled correctly.')
    
    return render(request, 'core/admin/inventory_form.html', {'action': 'Create'})


@admin_required
@require_http_methods(["GET", "POST"])
def inventory_edit(request, item_id):
    """Edit inventory item"""
    item = get_object_or_404(InventoryItem, id=item_id)
    
    if request.method == 'POST':
        try:
            item.name = request.POST.get('name')
            item.category = request.POST.get('category')
            item.quantity = int(request.POST.get('quantity', 0))
            item.low_stock_threshold = int(request.POST.get('low_stock_threshold', 10))
            item.save()
            messages.success(request, f'Inventory item "{item.name}" has been successfully updated!')
            return redirect('admin_inventory')
        except ValueError as e:
            messages.error(request, 'Please check your input. Quantity and threshold must be valid numbers.')
        except Exception as e:
            messages.error(request, 'Unable to update inventory item. Please verify all required fields are filled correctly.')
    
    return render(request, 'core/admin/inventory_form.html', {'item': item, 'action': 'Edit'})


@admin_required
@require_http_methods(["GET", "POST"])
def inventory_update_stock(request, item_id):
    """Update inventory stock"""
    item = get_object_or_404(InventoryItem, id=item_id)
    
    if request.method == 'POST':
        try:
            change = int(request.POST.get('quantity_change', 0))
            item.quantity += change
            if item.quantity < 0:
                item.quantity = 0
            item.save()
            messages.success(request, f'Stock updated successfully! "{item.name}" now has {item.quantity} units in inventory.')
            return redirect('admin_inventory')
        except ValueError as e:
            messages.error(request, 'Please enter a valid number for the quantity change.')
        except Exception as e:
            messages.error(request, 'Unable to update stock. Please try again.')
    
    return render(request, 'core/admin/inventory_update_stock.html', {'item': item})


@admin_required
def inventory_delete(request, item_id):
    """Delete inventory item"""
    item = get_object_or_404(InventoryItem, id=item_id)
    if request.method == 'POST':
        item_name = item.name
        item.delete()
        messages.success(request, f'Inventory item "{item_name}" has been successfully removed from inventory.')
        return redirect('admin_inventory')
    return render(request, 'core/admin/inventory_confirm_delete.html', {'item': item})


@admin_required
def admin_finances(request):
    """Finances management view"""
    expenditures = Expenditure.objects.all()
    class_needs = ClassNeed.objects.all()
    total_donations = Donor.objects.aggregate(Sum('total_donated'))['total_donated__sum'] or Decimal('0')
    total_expenditure = expenditures.aggregate(Sum('amount'))['amount__sum'] or Decimal('0')
    total_needs = sum(need.total for need in class_needs)
    available_funds = get_available_funds()
    
    return render(request, 'core/admin/finances.html', {
        'expenditures': expenditures,
        'class_needs': class_needs,
        'total_donations': total_donations,
        'total_expenditure': total_expenditure,
        'total_needs': total_needs,
        'available_funds': available_funds,
    })


@admin_required
@require_http_methods(["GET", "POST"])
def expenditure_create(request):
    """Create new expenditure"""
    if request.method == 'POST':
        try:
            expense_amount = Decimal(str(request.POST.get('amount', 0)))
            available_funds = get_available_funds()
            
            if expense_amount <= 0:
                messages.error(request, 'Expenditure amount must be greater than zero.')
            elif expense_amount > available_funds:
                messages.error(request, f'Insufficient funds! Available: ₹{float(available_funds):.2f}, Requested: ₹{float(expense_amount):.2f}')
            else:
                expenditure = Expenditure.objects.create(
                    description=request.POST.get('description'),
                    amount=expense_amount,
                    date=request.POST.get('date'),
                    category=request.POST.get('category', 'Supplies')
                )
                messages.success(request, f'Expenditure "{expenditure.description}" has been successfully recorded!')
                return redirect('admin_finances')
        except ValueError as e:
            messages.error(request, 'Please check your input. Amount must be a valid number and date must be in correct format.')
        except Exception as e:
            messages.error(request, 'Unable to create expenditure. Please verify all required fields are filled correctly.')
    
    available_funds = get_available_funds()
    return render(request, 'core/admin/expenditure_form.html', {
        'action': 'Create',
        'available_funds': available_funds
    })


@admin_required
@require_http_methods(["GET", "POST"])
def expenditure_edit(request, expenditure_id):
    """Edit expenditure"""
    expenditure = get_object_or_404(Expenditure, id=expenditure_id)
    
    if request.method == 'POST':
        try:
            new_amount = Decimal(str(request.POST.get('amount', 0)))
            old_amount = Decimal(str(expenditure.amount))
            available_funds = get_available_funds()
            
            # Calculate the difference: if increasing amount, check if we have enough funds
            amount_difference = new_amount - old_amount
            new_available_funds = available_funds - amount_difference
            
            if new_amount <= 0:
                messages.error(request, 'Expenditure amount must be greater than zero.')
            elif new_available_funds < 0:
                messages.error(request, f'Insufficient funds! Available: ₹{float(available_funds):.2f}, Additional needed: ₹{float(-new_available_funds):.2f}')
            else:
                expenditure.description = request.POST.get('description')
                expenditure.amount = new_amount
                expenditure.date = request.POST.get('date')
                expenditure.category = request.POST.get('category', 'Supplies')
                expenditure.save()
                messages.success(request, f'Expenditure "{expenditure.description}" has been successfully updated!')
                return redirect('admin_finances')
        except ValueError as e:
            messages.error(request, 'Please check your input. Amount must be a valid number and date must be in correct format.')
        except Exception as e:
            messages.error(request, 'Unable to update expenditure. Please verify all required fields are filled correctly.')
    
    available_funds = get_available_funds()
    return render(request, 'core/admin/expenditure_form.html', {
        'expenditure': expenditure,
        'action': 'Edit',
        'available_funds': available_funds
    })


@admin_required
def expenditure_delete(request, expenditure_id):
    """Delete expenditure"""
    expenditure = get_object_or_404(Expenditure, id=expenditure_id)
    if request.method == 'POST':
        desc = expenditure.description
        expenditure.delete()
        messages.success(request, f'Expenditure "{desc}" has been successfully removed from the records.')
        return redirect('admin_finances')
    return render(request, 'core/admin/expenditure_confirm_delete.html', {'expenditure': expenditure})


@admin_required
@require_http_methods(["GET", "POST"])
def classneed_create(request):
    """Create new class need"""
    if request.method == 'POST':
        try:
            classneed = ClassNeed.objects.create(
                class_name=request.POST.get('class_name'),
                item=request.POST.get('item'),
                quantity_needed=int(request.POST.get('quantity_needed', 0)),
                cost_per_item=float(request.POST.get('cost_per_item', 0))
            )
            messages.success(request, f'Class need for "{classneed.item}" (Grade {classneed.class_name}) has been successfully added!')
            return redirect('admin_finances')
        except ValueError as e:
            messages.error(request, 'Please check your input. Quantity and cost must be valid numbers.')
        except Exception as e:
            messages.error(request, 'Unable to create class need. Please verify all required fields are filled correctly.')
    
    return render(request, 'core/admin/classneed_form.html', {'action': 'Create'})


@admin_required
@require_http_methods(["GET", "POST"])
def classneed_edit(request, classneed_id):
    """Edit class need"""
    classneed = get_object_or_404(ClassNeed, id=classneed_id)
    
    if request.method == 'POST':
        try:
            classneed.class_name = request.POST.get('class_name')
            classneed.item = request.POST.get('item')
            classneed.quantity_needed = int(request.POST.get('quantity_needed', 0))
            classneed.cost_per_item = float(request.POST.get('cost_per_item', 0))
            classneed.save()
            messages.success(request, f'Class need for "{classneed.item}" has been successfully updated!')
            return redirect('admin_finances')
        except ValueError as e:
            messages.error(request, 'Please check your input. Quantity and cost must be valid numbers.')
        except Exception as e:
            messages.error(request, 'Unable to update class need. Please verify all required fields are filled correctly.')
    
    return render(request, 'core/admin/classneed_form.html', {'classneed': classneed, 'action': 'Edit'})


@admin_required
def classneed_delete(request, classneed_id):
    """Delete class need"""
    classneed = get_object_or_404(ClassNeed, id=classneed_id)
    if request.method == 'POST':
        item = classneed.item
        classneed.delete()
        messages.success(request, f'Class need "{item}" has been successfully removed from the records.')
        return redirect('admin_finances')
    return render(request, 'core/admin/classneed_confirm_delete.html', {'classneed': classneed})


@require_http_methods(["GET", "POST"])
def donor_registration(request):
    """Donor registration view"""
    from datetime import datetime
    import re
    from django.core.validators import validate_email
    from django.core.exceptions import ValidationError
    
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        mobile_number = request.POST.get('mobileNumber', '').strip()
        address = request.POST.get('address', '').strip()
        password = request.POST.get('password', '').strip()
        
        # Validate name
        if not name:
            messages.error(request, 'Name is required.')
        # Validate email
        elif not email:
            messages.error(request, 'Email is required.')
        else:
            # Validate email format
            try:
                validate_email(email)
            except ValidationError:
                messages.error(request, 'Please enter a valid email address.')
                return render(request, 'core/donor_registration.html', {
                    'current_year': datetime.now().year
                })
            
            # Check if email already exists
            if RegisteredDonor.objects.filter(email=email).exists():
                messages.error(request, 'This email is already registered. Please use a different email address.')
            # Validate password
            elif not password:
                messages.error(request, 'Password is required.')
            else:
                # Password validation: minimum 6 characters, one capital, one small, one special character, one number
                password_errors = []
                if len(password) < 6:
                    password_errors.append('Password must be at least 6 characters long.')
                if not re.search(r'[A-Z]', password):
                    password_errors.append('Password must contain at least one capital letter.')
                if not re.search(r'[a-z]', password):
                    password_errors.append('Password must contain at least one small letter.')
                if not re.search(r'[0-9]', password):
                    password_errors.append('Password must contain at least one number.')
                if not re.search(r'[!@#$%^&*()_+\-=\[\]{};\':"\\|,.<>\/?]', password):
                    password_errors.append('Password must contain at least one special character (!@#$%^&* etc.).')
                
                if password_errors:
                    messages.error(request, 'Password validation failed: ' + ' '.join(password_errors))
                else:
                    # Get security question and answer
                    security_question = request.POST.get('security_question', '').strip()
                    security_answer = request.POST.get('security_answer', '').strip()
                    
                    if not security_question:
                        messages.error(request, 'Security question is required.')
                    elif not security_answer:
                        messages.error(request, 'Security answer is required.')
                    else:
                        # All validations passed, create donor
                        donor = RegisteredDonor(
                            name=name,
                            email=email,
                            mobile_number=mobile_number,
                            address=address,
                            security_question=security_question,
                            security_answer=security_answer.lower().strip()
                        )
                        donor.set_password(password)
                        donor.save()
                        messages.success(request, 'Registration successful! Welcome to BrightFutures. You will be redirected to the login page shortly.')
                        return redirect('donor_login')
    
    return render(request, 'core/donor_registration.html', {
        'current_year': datetime.now().year
    })


@require_http_methods(["GET", "POST"])
def donor_login(request):
    """Donor login view"""
    from datetime import datetime
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        if not email or not password:
            messages.error(request, 'Please provide both email and password.')
        else:
            from .models import RegisteredDonor
            try:
                donor = RegisteredDonor.objects.get(email=email)
                
                if donor.check_password(password):
                    from django.db import connection
                    donor_id = donor.id
                    try:
                        desired_donation_val = donor.desired_donation
                        if desired_donation_val:
                            try:
                                desired_decimal = Decimal(str(desired_donation_val))
                                if desired_decimal > Decimal('1000000'):
                                    with connection.cursor() as fix_cursor:
                                        fix_cursor.execute("""
                                            UPDATE core_registereddonor
                                            SET desired_donation = 0
                                            WHERE id = %s
                                        """, [donor_id])
                            except (ValueError, InvalidOperation, TypeError):
                                with connection.cursor() as fix_cursor:
                                    fix_cursor.execute("""
                                        UPDATE core_registereddonor
                                        SET desired_donation = 0
                                        WHERE id = %s
                                    """, [donor_id])
                    except (ValueError, InvalidOperation, TypeError):
                        pass
                    
                    donor = RegisteredDonor.objects.get(id=donor_id)
                    request.session['donor_id'] = donor.id
                    request.session['donor_authenticated'] = True
                    request.session['last_activity'] = datetime.now().isoformat()
                    return redirect('donor_dashboard')
                else:
                    messages.error(request, 'Invalid email or password. Please try again.')
            except RegisteredDonor.DoesNotExist:
                messages.error(request, 'Invalid email or password. Please try again.')
            except Exception as e:
                # If there's still an error, try to fix the database and retry
                messages.error(request, 'An error occurred during login. Please try again.')
                import logging
                logging.error(f"Donor login error: {e}")
    
    return render(request, 'core/donor_login.html', {
        'current_year': datetime.now().year
    })


@require_http_methods(["GET", "POST"])
def donor_forgot_password(request):
    """Donor forgot password - step 1: request email and show security question"""
    from datetime import datetime
    from .models import RegisteredDonor
    
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        
        if not email:
            messages.error(request, 'Please enter your email address.')
        else:
            try:
                donor = RegisteredDonor.objects.get(email=email)
                
                # Store donor info in session for password reset
                request.session['password_reset_user_type'] = 'donor'
                request.session['password_reset_user_id'] = donor.id
                request.session['password_reset_email'] = email
                request.session['password_reset_attempts'] = 0
                
                # Redirect to security question page
                return redirect('donor_verify_security')
            except RegisteredDonor.DoesNotExist:
                # Don't reveal if email exists or not for security
                messages.error(request, 'If an account exists with this email, you will be shown a security question.')
            except Exception as e:
                messages.error(request, 'An error occurred. Please try again.')
    
    return render(request, 'core/donor_forgot_password.html', {
        'current_year': datetime.now().year
    })


@require_http_methods(["GET", "POST"])
def donor_verify_security(request):
    """Donor verify security question - step 2: verify security answer"""
    from datetime import datetime
    from .models import RegisteredDonor
    
    # Check if user is in password reset flow
    if request.session.get('password_reset_user_type') != 'donor':
        messages.error(request, 'Please request a password reset first.')
        return redirect('donor_forgot_password')
    
    donor_id = request.session.get('password_reset_user_id')
    if not donor_id:
        messages.error(request, 'Session expired. Please start again.')
        return redirect('donor_forgot_password')
    
    try:
        donor = RegisteredDonor.objects.get(id=donor_id)
    except RegisteredDonor.DoesNotExist:
        messages.error(request, 'Account not found. Please try again.')
        request.session.pop('password_reset_user_type', None)
        request.session.pop('password_reset_user_id', None)
        request.session.pop('password_reset_email', None)
        return redirect('donor_forgot_password')
    
    attempts = request.session.get('password_reset_attempts', 0)
    
    # Check if max attempts exceeded
    if attempts >= 3:
        messages.error(request, 'Maximum attempts exceeded. Please contact support.')
        request.session.pop('password_reset_user_type', None)
        request.session.pop('password_reset_user_id', None)
        request.session.pop('password_reset_email', None)
        request.session.pop('password_reset_attempts', None)
        return redirect('donor_forgot_password')
    
    if request.method == 'POST':
        security_answer = request.POST.get('security_answer', '').strip().lower()
        
        if not security_answer:
            messages.error(request, 'Please enter your security answer.')
        else:
            # Compare answers (case-insensitive)
            if security_answer == donor.security_answer.lower().strip():
                # Security answer verified successfully
                request.session['password_reset_verified'] = True
                request.session.pop('password_reset_attempts', None)
                messages.success(request, 'Security answer verified. Please set your new password.')
                return redirect('donor_reset_password')
            else:
                # Increment attempts
                request.session['password_reset_attempts'] = attempts + 1
                remaining = 3 - (attempts + 1)
                if remaining > 0:
                    messages.error(request, f'Incorrect security answer. {remaining} attempt(s) remaining.')
                else:
                    messages.error(request, 'Maximum attempts exceeded. Please contact support.')
                    request.session.pop('password_reset_user_type', None)
                    request.session.pop('password_reset_user_id', None)
                    request.session.pop('password_reset_email', None)
                    request.session.pop('password_reset_attempts', None)
                    return redirect('donor_forgot_password')
    
    return render(request, 'core/donor_verify_security.html', {
        'current_year': datetime.now().year,
        'security_question': donor.security_question,
        'remaining_attempts': 3 - attempts
    })


@require_http_methods(["GET", "POST"])
def donor_reset_password(request):
    """Donor reset password - step 3: set new password"""
    from datetime import datetime
    import re
    
    # Check if security answer is verified
    if not request.session.get('password_reset_verified'):
        messages.error(request, 'Please verify your security answer first.')
        return redirect('donor_forgot_password')
    
    if request.session.get('password_reset_user_type') != 'donor':
        messages.error(request, 'Invalid session. Please start again.')
        return redirect('donor_forgot_password')
    
    donor_id = request.session.get('password_reset_user_id')
    
    if not donor_id:
        messages.error(request, 'Session expired. Please start again.')
        return redirect('donor_forgot_password')
    
    try:
        donor = RegisteredDonor.objects.get(id=donor_id)
    except RegisteredDonor.DoesNotExist:
        messages.error(request, 'Account not found. Please try again.')
        request.session.pop('password_reset_verified', None)
        request.session.pop('password_reset_email', None)
        request.session.pop('password_reset_user_type', None)
        request.session.pop('password_reset_user_id', None)
        return redirect('donor_forgot_password')
    
    if request.method == 'POST':
        new_password = request.POST.get('new_password', '').strip()
        confirm_password = request.POST.get('confirm_password', '').strip()
        
        if not new_password:
            messages.error(request, 'Please enter a new password.')
        elif not confirm_password:
            messages.error(request, 'Please confirm your new password.')
        elif new_password != confirm_password:
            messages.error(request, 'Passwords do not match. Please try again.')
        else:
            # Password validation: minimum 6 characters, one capital, one small, one special character, one number
            password_errors = []
            if len(new_password) < 6:
                password_errors.append('Password must be at least 6 characters long.')
            if not re.search(r'[A-Z]', new_password):
                password_errors.append('Password must contain at least one capital letter.')
            if not re.search(r'[a-z]', new_password):
                password_errors.append('Password must contain at least one small letter.')
            if not re.search(r'[0-9]', new_password):
                password_errors.append('Password must contain at least one number.')
            if not re.search(r'[!@#$%^&*()_+\-=\[\]{};\':"\\|,.<>\/?]', new_password):
                password_errors.append('Password must contain at least one special character (!@#$%^&* etc.).')
            
            if password_errors:
                messages.error(request, 'Password validation failed: ' + ' '.join(password_errors))
            else:
                donor.set_password(new_password)
                donor.save()
                
                # Clear all password reset session data
                request.session.pop('password_reset_verified', None)
                request.session.pop('password_reset_mobile', None)
                request.session.pop('password_reset_user_type', None)
                request.session.pop('password_reset_user_id', None)
                request.session.pop('password_reset_last_request', None)
                
                messages.success(request, 'Password reset successfully! Please login with your new password.')
                return redirect('donor_login')
    
    return render(request, 'core/donor_reset_password.html', {
        'current_year': datetime.now().year,
        'donor': donor
    })


def donor_logout(request):
    """Donor logout view"""
    request.session.pop('donor_id', None)
    request.session.pop('donor_authenticated', None)
    request.session.pop('last_activity', None)
    messages.success(request, 'You have been successfully logged out.')
    return redirect('home')


def donate(request):
    """Donation page with both login and registration options"""
    from datetime import datetime
    return render(request, 'core/donate.html', {
        'current_year': datetime.now().year
    })


def donor_required(view_func):
    """Decorator to check donor authentication"""
    def wrapper(request, *args, **kwargs):
        if not request.session.get('donor_authenticated'):
            return redirect('donor_login')
        return view_func(request, *args, **kwargs)
    return wrapper


@donor_required
def donor_dashboard(request):
    """Donor dashboard view"""
    donor_id = request.session.get('donor_id')
    try:
        donor = RegisteredDonor.objects.get(id=donor_id)
        class_needs = ClassNeed.objects.all()
        return render(request, 'core/donor_dashboard.html', {
            'donor': donor,
            'class_needs': class_needs,
            'donor_authenticated': True,
        })
    except RegisteredDonor.DoesNotExist:
        return redirect('donor_login')


@donor_required
@require_http_methods(["POST"])
def donor_update_donation(request):
    """Update donor's desired donation amount and frequency"""
    donor_id = request.session.get('donor_id')
    MAX_DONATION = Decimal('1000000')  # 10 Lakh
    try:
        donor = RegisteredDonor.objects.get(id=donor_id)
        donation_amount_str = request.POST.get('desired_donation', '0').strip()
        
        # Validate and convert to Decimal
        try:
            desired_donation = Decimal(str(donation_amount_str))
        except (ValueError, InvalidOperation):
            messages.error(request, 'Please enter a valid donation amount.')
            return redirect('donor_dashboard')
        
        donation_frequency = request.POST.get('donation_frequency', '').strip()
        
        if desired_donation < 0:
            messages.error(request, 'Donation amount cannot be negative.')
        elif desired_donation > MAX_DONATION:
            messages.error(request, f'Donation amount cannot exceed ₹10,00,000 (10 Lakh). Please enter a lower amount.')
        elif not donation_frequency:
            messages.error(request, 'Please select a recent donation frequency.')
            return redirect('donor_dashboard')
        else:
            donor.desired_donation = desired_donation
            donor.donation_frequency = donation_frequency
            donor.save()
            if desired_donation > 0:
                frequency_text = donation_frequency if donation_frequency != 'N/A' else 'one-time'
                messages.success(request, f'Your desired donation amount of ₹{desired_donation:.2f} ({frequency_text}) has been recorded. Our team will contact you soon!')
            else:
                messages.success(request, 'Your desired donation amount has been cleared.')
    except ValueError:
        messages.error(request, 'Please enter a valid donation amount.')
    except RegisteredDonor.DoesNotExist:
        messages.error(request, 'Unable to update donation. Please try again.')
    except Exception as e:
        messages.error(request, 'An error occurred. Please try again.')
    
    return redirect('donor_dashboard')


@donor_required
@require_http_methods(["POST"])
def donor_remove_donation(request):
    """Remove donor's desired donation amount (set to 0)"""
    donor_id = request.session.get('donor_id')
    try:
        from decimal import Decimal
        donor = RegisteredDonor.objects.get(id=donor_id)
        donor.desired_donation = Decimal('0')
        donor.save()
        # Refresh donor data in session or context to ensure fresh data on redirect
        messages.success(request, 'Your desired donation amount has been removed successfully.')
    except RegisteredDonor.DoesNotExist:
        messages.error(request, 'Unable to remove donation. Please try again.')
    except Exception as e:
        messages.error(request, 'Unable to remove donation. Please try again.')
    
    return redirect('donor_dashboard')


@donor_required
@require_http_methods(["GET", "POST"])
def donor_edit_profile(request):
    """Edit donor profile (email, mobile, address, password)"""
    donor_id = request.session.get('donor_id')
    try:
        donor = RegisteredDonor.objects.get(id=donor_id)
    except RegisteredDonor.DoesNotExist:
        messages.error(request, 'Unable to load your profile. Please try again.')
        return redirect('donor_dashboard')
    
    if request.method == 'POST':
        try:
            # Get form data
            new_email = request.POST.get('email', '').strip()
            new_mobile = request.POST.get('mobile_number', '').strip()
            new_address = request.POST.get('address', '').strip()
            new_password = request.POST.get('password', '').strip()
            new_security_question = request.POST.get('security_question', '').strip()
            new_security_answer = request.POST.get('security_answer', '').strip()
            
            # Validate email
            if not new_email:
                messages.error(request, 'Email is required.')
            # Check if email is being changed and if it's already taken
            elif new_email != donor.email:
                if RegisteredDonor.objects.filter(email=new_email).exists():
                    messages.error(request, 'This email is already registered. Please use a different email address.')
                else:
                    donor.email = new_email
            else:
                # Email not changed, keep it
                pass
            
            # Update mobile if provided
            if new_mobile:
                donor.mobile_number = new_mobile
            
            # Update address if provided
            if new_address:
                donor.address = new_address
            
            # Update password only if a new one is provided
            if new_password:
                donor.set_password(new_password)
            # If password is empty, keep the current password (don't update)
            
            # Update security question (required)
            if not new_security_question:
                messages.error(request, 'Security question is required.')
                return render(request, 'core/donor_edit_profile.html', {
                    'donor': donor,
                    'donor_authenticated': True,
                })
            else:
                donor.security_question = new_security_question
            
            # Update security answer (required)
            if not new_security_answer:
                messages.error(request, 'Security answer is required.')
                return render(request, 'core/donor_edit_profile.html', {
                    'donor': donor,
                    'donor_authenticated': True,
                })
            else:
                donor.security_answer = new_security_answer.lower().strip()  # Store as lowercase for case-insensitive comparison
            
            # Save donor
            donor.save()
            messages.success(request, 'Your profile has been successfully updated!')
            return redirect('donor_dashboard')
            
        except Exception as e:
            messages.error(request, 'Unable to update your profile. Please check your input and try again.')
    
    return render(request, 'core/donor_edit_profile.html', {
        'donor': donor,
        'donor_authenticated': True,
    })

