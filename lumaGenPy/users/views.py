from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
from .forms import SignupForm
from django.http import JsonResponse

###################################
def get_saved_topics(request):
    student_id = request.session.get('student_id')
    saved_topics = Save.objects.filter(student_id=student_id).select_related('topic')

    data = []
    for save in saved_topics:
        data.append({
            'title': save.topic.title,
            'image_url': save.topic.image_url,
            'saved_date': save.saved_date.isoformat(),  
            'student_id': save.student.id,
            'topic_id': save.topic.id,
        })

    return JsonResponse(data, safe=False)

def get_notes(request):
    student_id = request.session.get('student_id')
    notes = Note.objects.filter(student_id=student_id)

    data = []
    for note in notes:
        data.append({
            'title': note.title,
            'content': note.content,
            'last_edited': note.last_edited.isoformat(),  
            'key_takeaway': note.key_takeaway,
            'note_id': note.id  
        })

    return JsonResponse(data, safe=False)

def get_likes(request):
    student_id = request.session.get('student_id')
    liked_content = Like.objects.filter(student_id=student_id).select_related('topic')

    data = []
    for like in liked_content:
        data.append({
            'title': like.topic.title,
            'image_url': like.topic.image_url,
            'like_id': like.id, 
            'topic_id': like.topic.id
        })

    return JsonResponse(data, safe=False)

#################################################3


def check_email(request):
    email = request.GET.get('email', None)
    if email:
        exists = User.objects.filter(email=email).exists()
        return JsonResponse({'exists': exists})
    return JsonResponse({'exists': False})

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from .forms import SignupForm
from .models import Students

# def signup_view(request):
#     if request.method == 'POST':
#         form = SignupForm(request.POST)

#         if form.is_valid():
#             # Save the student instance with a hashed password
#             student = Students(
#                 student_password= form.cleaned_data['password'],
#                 first_name=form.cleaned_data['first_name'],
#                 last_name=form.cleaned_data['last_name'],
#                 email=form.cleaned_data['email']
#             )
#             student.save()

#             messages.success(request, "Account created successfully.")
#             return redirect('login')  # Use the URL name or appropriate URL pattern

#         else:
#             for error in form.errors.values():
#                 messages.error(request, error)

#     else:
#         form = SignupForm()

#     return render(request, 'signup.html', {'form': form})
def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)

        if form.is_valid():
            # Create an instance of the student and hash the password
            student = Students(
                student_password=make_password(form.cleaned_data['password']),  # Hashing the password
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                email=form.cleaned_data['email']
            )
            student.save()

            messages.success(request, "Account created successfully.")
            return redirect('login')  # Redirect to the login page or appropriate URL pattern

        else:
            # Display error messages for invalid form
            for error in form.errors.values():
                messages.error(request, error)

    else:
        form = SignupForm()  # Create a new form instance for GET requests

    return render(request, 'signup.html', {'form': form})  # Render the signup template



def home_view(request):
    return render(request, 'homepage.html')

def about_view(request):
    return render(request, 'about.html')


# def login_view(request):
#     if request.method == "POST":
#         email = request.POST.get('email')
#         password = request.POST.get('password')

        
#         try:
#             user = Students.objects.get(email=email)
#             if password == user.student_password:  # Verify password
                
#                 return redirect('user_page')  # Redirect to homepage
#             else:
#                 messages.error(request, "Invalid password.")
#         except Students.DoesNotExist:
#             messages.error(request, "User does not exist.")
    
#     return render(request, 'login.html')  # Render your login template



def login_view(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = Students.objects.get(email=email)
            if password == user.student_password:  # Verify password
                # Store the full name in the session
                request.session['full_name'] = f"{user.first_name} {user.last_name}"  # Adjust according to your model's field names
                request.session['email'] = user.email
                return redirect('user_page')  # Redirect to user homepage
            else:
                messages.error(request, "Invalid password.")
        except Students.DoesNotExist:
            messages.error(request, "User does not exist.")
    
    return render(request, 'login.html')  # Render the login template





def adminlogin_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            admin = Admins.objects.get(email=email)
            if  password == admin.admin_password:  
                full_name = f"{admin.first_name} {admin.last_name}"
                request.session['full_name'] = f"{admin.first_name} {admin.last_name}"
                messages.success(request, "Login successful!")
                return render(request, 'admin_page.html', {'full_name': full_name})
                #messages.success(request, "Login successful!")
                 
            else:
                messages.error(request, "Invalid password.")
        except Admins.DoesNotExist:
            messages.error(request, "Email not registered.")

    return render(request, 'adminlogin.html')


def check_user(email, password):
    try:
        user = Students.objects.get(email=email)
        return (password, user.password)
    except User.DoesNotExist:
        return False
    


 
def homepage_view(request):
    context = {
        'some_key': 'some_value',
        'another_key': 'another_value',
        
    }
    return render(request, 'homepage.html') 

def topics_view(request):
    return render(request, 'topics.html')

#topics view: 

def algorthim_view(request):
    return render(request, 'algorthim.html') 
def computer_org_view(request):
    return render(request, 'computer_org.html') 
def  history_computing_view(request):
    return render(request, 'history_computing.html') 
def logic_proof_view(request):
    return render(request, 'logic_proof.html') 
def operating_systems_view(request):
    return render(request, 'operating_systems.html') 
def software_eng_view(request):
    return render(request, 'software_eng.html') 

###
def role_view(request):
    return render(request, 'role.html') 

#########
def get_full_name(request):
    """ function to get the full name of the authenticated admin."""
    if request.user.is_authenticated:
        try:
            admin = Admins.objects.get(email=request.user.email)
            return f"{admin.first_name} {admin.last_name}"
        except Admins.DoesNotExist:
            return ''  # Return an empty string if not found
    return ''  

def users_view(request):
    full_name = request.session.get('full_name', '')  
    email = request.session.get('email', '')
    context = {
        'full_name': full_name,
        'email': email,
    }
    return render(request, 'users.html', context)

def admin_view(request):
    full_name = request.session.get('full_name', '')  
    context = {
        'full_name': full_name,
    }
    return render(request, 'admin_page.html', context)

def setting_view(request):
    full_name = request.session.get('full_name', '')  
    context = {
        'full_name': full_name,
    }
    return render(request, 'setting.html', context)

# def editprofile_view(request):
#     full_name = request.session.get('full_name', '')  
#     email = request.session.get('email', '')
#     print("Full Name:", full_name)  # Debugging
#     print("Email:", email)
#     context = {
#         'full_name': full_name,
#         'email': email,
#     }
#     return render(request, 'editprofile.html', context)

def editprofile_view(request):
    if request.method == "POST":
        # Get the data from the form
        name = request.POST.get('name')
        email = request.POST.get('email')
        
        
        # Update the student's information
        try:
            user = Students.objects.get(email=request.session.get('email'))  
            user.first_name, user.last_name = name.split(" ")  # Update full name
            user.email = email  # Update email
            
            user.save()  
            
            # Update the session values
            request.session['full_name'] = name
            request.session['email'] = email
            
            messages.success(request, "Profile updated successfully!")
            return redirect('user_page')  # Redirect to user page after updating
        
        except Students.DoesNotExist:
            messages.error(request, "User does not exist.")
            return redirect('editprofile')  # Redirect back to edit profile if user doesn't exist

    
    full_name = request.session.get('full_name', '')
    email = request.session.get('email', '')
    context = {
        'full_name': full_name,
        'email': email,
    }
    return render(request, 'editprofile.html', context)
   





# def user_page_view(request):
#     return render(request, 'user_page.html')

# def user_page_view(request):
#     full_name = request.session.get('full_name', '')  # Get full name from session
#     context = {
#         'full_name': full_name,
#     }
#     return render(request, 'user_page.html', context)



def user_page_view(request):
    full_name = request.session.get('full_name', '')  
    email = request.session.get('email', '')
    user = request.user 
    student_id = request.session.get('student_id')  

    # Fetch data from the database
    saved_topics = Save.objects.filter(student=student_id)  
    notes = Note.objects.filter(student=student_id)
    liked_content = Like.objects.filter(student=student_id)

    # Prepare context with full name and content
    context = {
        'full_name': full_name,
        'saved_topics': saved_topics,
        'notes': notes,
        'liked_content': liked_content,
        'email' : email,
    }
    
    return render(request, 'user_page.html', context)