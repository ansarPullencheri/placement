from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import UserProfile, CompanyRegistration, CandidateRegistration

# ------------------ Public Views ------------------

def main(request):
    return render(request, 'web/main.html')

def index(request):
    return render(request, 'web/index.html')

def candidate(request):
    return render(request, 'web/candidate.html')

def user_login(request):
    # If user is already authenticated
    if request.user.is_authenticated:
        profile = getattr(request.user, 'profile', None)  # Safe way to get profile
        if profile and profile.user_type == 'admin':
            return redirect('web:dashboard')
        else:
            logout(request)
            messages.error(request, 'Admin access only.')
            return redirect('web:login')
    
    # Handle login POST request
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            profile = getattr(user, 'profile', None)
            if profile and profile.user_type == 'admin':
                login(request, user)
                messages.success(request, 'Welcome Admin!')
                return redirect('web:dashboard')
            else:
                messages.error(request, 'Access denied. Admin login only.')
                return redirect('web:login')
        else:
            messages.error(request, 'Invalid username or password.')
    
    # Default: render login page
    return render(request, 'web/login.html')

    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            try:
                profile = user.profile
                if profile.user_type == 'admin':
                    login(request, user)
                    messages.success(request, 'Welcome Admin!')
                    return redirect('web:dashboard')
                else:
                    messages.error(request, 'Access denied. Admin login only.')
                    return redirect('web:login')
            except UserProfile.DoesNotExist:
                messages.error(request, 'User profile not found.')
                return redirect('web:login')
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'web/login.html')

@login_required
def user_logout(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('web:main')

# ------------------ Admin Dashboard ------------------

@login_required
def dashboard(request):
    try:
        if request.user.profile.user_type != 'admin':
            messages.error(request, 'Access denied. Admin only.')
            logout(request)
            return redirect('web:login')
    except:
        messages.error(request, 'Access denied.')
        logout(request)
        return redirect('web:login')
    
    total_companies = CompanyRegistration.objects.count()
    total_candidates = CandidateRegistration.objects.count()
    recent_companies = CompanyRegistration.objects.order_by('-created_at')[:5]
    recent_candidates = CandidateRegistration.objects.order_by('-created_at')[:5]
    
    context = {
        'total_companies': total_companies,
        'total_candidates': total_candidates,
        'recent_companies': recent_companies,
        'recent_candidates': recent_candidates,
    }
    
    return render(request, 'web/dashboard.html', context)

# ------------------ API Endpoints ------------------

@csrf_exempt
def submit_company_registration(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            company = CompanyRegistration.objects.create(
                interview_date=data['interviewDate'],
                company_name=data['companyName'],
                contact_person=data['contactPerson'],
                designation=data['designation'],
                email=data['email'],
                whatsapp=data['whatsapp'],
                mobile=data['mobile'],
                location=data['location'],
                post=data['post'],
                vacancies=data['vacancies'],
                salary=data['salary']
            )
            return JsonResponse({'status': 'success', 'message': 'Company registered successfully!'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)

@csrf_exempt
def submit_candidate_registration(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            # Validate required fields
            required_fields = ['name', 'dob', 'gender', 'category', 'district', 
                             'postOffice', 'mobile', 'email', 'trade', 
                             'passoutYear', 'institute', 'experience']
            
            for field in required_fields:
                if field not in data or not data[field]:
                    return JsonResponse({
                        'status': 'error', 
                        'message': f'Missing required field: {field}'
                    }, status=400)
            
            candidate = CandidateRegistration.objects.create(
                name=data['name'],
                dob=data['dob'],
                gender=data['gender'],
                category=data['category'],
                district=data['district'],
                post_office=data['postOffice'],
                mobile=data['mobile'],
                email=data['email'],
                trade=data['trade'],
                passout_year=data['passoutYear'],
                institute=data['institute'],
                experience=data['experience']
            )
            return JsonResponse({
                'status': 'success', 
                'message': 'Candidate registered successfully!',
                'candidate_id': candidate.id
            })
        except json.JSONDecodeError:
            return JsonResponse({
                'status': 'error', 
                'message': 'Invalid JSON data'
            }, status=400)
        except Exception as e:
            return JsonResponse({
                'status': 'error', 
                'message': f'Error: {str(e)}'
            }, status=400)
    return JsonResponse({
        'status': 'error', 
        'message': 'Invalid request method'
    }, status=400)

# ------------------ Admin Management Views ------------------

@login_required
def view_companies(request):
    if request.user.profile.user_type != 'admin':
        messages.error(request, 'Access denied. Admin only.')
        return redirect('web:main')
    
    companies = CompanyRegistration.objects.all().order_by('-created_at')
    return render(request, 'web/view_companies.html', {'companies': companies})

@login_required
def view_candidates(request):
    if request.user.profile.user_type != 'admin':
        messages.error(request, 'Access denied. Admin only.')
        return redirect('web:main')
    
    candidates = CandidateRegistration.objects.all().order_by('-created_at')
    return render(request, 'web/view_candidates.html', {'candidates': candidates})

@login_required
def delete_company(request, company_id):
    if request.user.profile.user_type != 'admin':
        messages.error(request, 'Access denied.')
        return redirect('web:main')
    
    try:
        company = CompanyRegistration.objects.get(id=company_id)
        company.delete()
        messages.success(request, 'Company deleted successfully.')
    except CompanyRegistration.DoesNotExist:
        messages.error(request, 'Company not found.')
    
    return redirect('web:view_companies')

@login_required
def delete_candidate(request, candidate_id):
    if request.user.profile.user_type != 'admin':
        messages.error(request, 'Access denied.')
        return redirect('web:main')
    
    try:
        candidate = CandidateRegistration.objects.get(id=candidate_id)
        candidate.delete()
        messages.success(request, 'Candidate deleted successfully.')
    except CandidateRegistration.DoesNotExist:
        messages.error(request, 'Candidate not found.')
    
    return redirect('web:view_candidates')
