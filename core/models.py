from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password, check_password, is_password_usable


class Admin(models.Model):
    email = models.EmailField(unique=True)
    mobile_number = models.CharField(max_length=20, blank=True, null=True, help_text="Mobile number with country code (e.g., +91XXXXXXXXXX)")
    password_plaintext = models.CharField(max_length=200)
    name = models.CharField(max_length=200, default='Admin')
    security_question = models.CharField(max_length=200, default='What is the name of your first pet?', help_text="Security question for password recovery")
    security_answer = models.CharField(max_length=100, default='admin123', help_text="Answer to security question (case-insensitive)")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Admin'
        verbose_name_plural = 'Admins'
    
    def set_password(self, raw_password):
        self.password_plaintext = make_password(raw_password)
    
    def check_password(self, raw_password):
        if not self.password_plaintext or not raw_password:
            return False
        # Check if password is hashed
        if is_password_usable(self.password_plaintext):
            # Password is hashed, use Django's check_password
            return check_password(raw_password, self.password_plaintext)
        else:
            # Password is still in plaintext (backward compatibility)
            return self.password_plaintext == raw_password
    
    def __str__(self):
        return self.email


class Student(models.Model):
    PERFORMANCE_CHOICES = [
        ('Excellent', 'Excellent'),
        ('Good', 'Good'),
        ('Average', 'Average'),
        ('Needs Improvement', 'Needs Improvement'),
    ]
    
    SPONSORSHIP_STATUS_CHOICES = [
        ('Sponsored', 'Sponsored'),
        ('Not Sponsored', 'Not Sponsored'),
    ]
    
    name = models.CharField(max_length=200)
    age = models.IntegerField()
    class_name = models.CharField(max_length=100)
    school = models.CharField(max_length=200)
    parental_income = models.DecimalField(max_digits=10, decimal_places=2)
    help_provided = models.TextField(help_text="Kind of help provided (e.g., books, money, school dress)")
    performance = models.CharField(max_length=20, choices=PERFORMANCE_CHOICES, default='Average')
    sponsorship_status = models.CharField(max_length=20, choices=SPONSORSHIP_STATUS_CHOICES, default='Not Sponsored')
    sponsor = models.ForeignKey('RegisteredDonor', on_delete=models.SET_NULL, null=True, blank=True, related_name='sponsored_students')
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female')], blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name


class Donor(models.Model):
    DONOR_TYPE_CHOICES = [
        ('Individual', 'Individual'),
        ('Corporate', 'Corporate'),
    ]
    
    name = models.CharField(max_length=200)
    donor_type = models.CharField(max_length=20, choices=DONOR_TYPE_CHOICES, default='Individual')
    total_donated = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    last_donation_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-total_donated']
    
    def __str__(self):
        return self.name


class RegisteredDonor(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    mobile_number = models.CharField(max_length=20)
    address = models.TextField()
    password_plaintext = models.CharField(max_length=200)
    security_question = models.CharField(max_length=200, blank=True, null=True, help_text="Security question for password recovery")
    security_answer = models.CharField(max_length=100, blank=True, null=True, help_text="Answer to security question (case-insensitive)")
    donation_frequency = models.CharField(
        max_length=20,
        choices=[
            ('Annual', 'Annual'),
            ('Half-yearly', 'Half-yearly'),
            ('N/A', 'N/A (One-time donor)')
        ],
        blank=True,
        null=True
    )
    amount_pledged = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_donated = models.DecimalField(max_digits=12, decimal_places=2, default=0, help_text="Total amount donated so far")
    desired_donation = models.DecimalField(max_digits=12, decimal_places=2, default=0, help_text="Amount donor currently wants to donate")
    last_donation_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def set_password(self, raw_password):
        self.password_plaintext = make_password(raw_password)
    
    def check_password(self, raw_password):
        if not self.password_plaintext or not raw_password:
            return False
        # Check if password is hashed
        if is_password_usable(self.password_plaintext):
            # Password is hashed, use Django's check_password
            return check_password(raw_password, self.password_plaintext)
        else:
            # Password is still in plaintext (backward compatibility)
            return self.password_plaintext == raw_password
    
    def __str__(self):
        return self.name


class InventoryItem(models.Model):
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=100)
    quantity = models.IntegerField(default=0)
    low_stock_threshold = models.IntegerField(default=10)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} ({self.category})"
    
    @property
    def is_low_stock(self):
        return self.quantity <= self.low_stock_threshold


class Expenditure(models.Model):
    CATEGORY_CHOICES = [
        ('Supplies', 'Supplies'),
        ('Utilities', 'Utilities'),
        ('Staff', 'Staff'),
        ('Maintenance', 'Maintenance'),
    ]
    
    description = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='Supplies')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-date']
    
    def __str__(self):
        return f"{self.description} - {self.amount}"


class ClassNeed(models.Model):
    class_name = models.CharField(max_length=100)
    item = models.CharField(max_length=200)
    quantity_needed = models.IntegerField()
    cost_per_item = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['class_name']
    
    @property
    def total(self):
        return self.quantity_needed * self.cost_per_item
    
    def __str__(self):
        return f"{self.item} for {self.class_name}"

