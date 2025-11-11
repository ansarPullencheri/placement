from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    USER_TYPE_CHOICES = (
        ('admin', 'Admin'),
        ('company', 'Company'),
        ('candidate', 'Candidate'),
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='candidate')
    phone = models.CharField(max_length=15, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.user_type}"

class CompanyRegistration(models.Model):
    interview_date = models.DateField()
    company_name = models.CharField(max_length=200)
    contact_person = models.CharField(max_length=100)
    designation = models.CharField(max_length=100)
    email = models.EmailField()
    whatsapp = models.CharField(max_length=15)
    mobile = models.CharField(max_length=15)
    location = models.CharField(max_length=200)
    post = models.CharField(max_length=100)
    vacancies = models.IntegerField()
    salary = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.company_name} - {self.post}"

class CandidateRegistration(models.Model):
    GENDER_CHOICES = (
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    )
    
    CATEGORY_CHOICES = (
        ('general', 'General'),
        ('obc', 'OBC'),
        ('sc', 'SC'),
        ('st', 'ST'),
        ('ews', 'EWS'),
    )
    
    name = models.CharField(max_length=200)
    dob = models.DateField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    district = models.CharField(max_length=100)
    post_office = models.CharField(max_length=100)
    mobile = models.CharField(max_length=15)
    email = models.EmailField()
    trade = models.CharField(max_length=100)
    passout_year = models.IntegerField()
    institute = models.CharField(max_length=300)
    experience = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} - {self.trade}"