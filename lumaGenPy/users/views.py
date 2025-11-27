from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User
#from django.contrib.auth.hashers import check_password  
from .forms import SignupForm
from django.http import JsonResponse

def check_email(request):
    email = request.GET.get('email', None)
    if email:
        exists = User.objects.filter(email=email).exists()
        return JsonResponse({'exists': exists})
    return JsonResponse({'exists': False})


def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            # Check if the email already exists
            email = form.cleaned_data['email']  # Get the email from the cleaned data
            if User.objects.filter(email=email).exists():
                form.add_error('email', 'An account with this email already exists.')
            else:
                # Create the user
                user = form.save(commit=False)
                user.password = form.cleaned_data['password']  # Store the plain password
                user.save()  # Save the user to the database
                messages.success(request, "Account created successfully!")
                return redirect('login')  # Redirect to the login page

    else:
        form = SignupForm()

    return render(request, 'signup.html', {'form': form})

def home_view(request):
    return render(request, 'homepage.html')




def login_view(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Check if the user exists in the database
        try:
            user = User.objects.get(email=email)
            if password == user.password:  # Verify password
                return redirect('homepage')  # Redirect to homepage
            else:
                messages.error(request, "Invalid password.")
        except User.DoesNotExist:
            messages.error(request, "User does not exist.")
    
    return render(request, 'login.html')  # Render your login template



def check_user(email, password):
    try:
        user = User.objects.get(email=email)
        return (password, user.password)
    except User.DoesNotExist:
        return False
    


 
def homepage_view(request):
    return render(request, 'homepage.html') 

def topics_view(request):
    return render(request, 'topics.html')
from django.shortcuts import render

