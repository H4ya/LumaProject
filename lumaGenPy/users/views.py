from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Q
from .models import *
import array as arr
from .forms import SignupForm
from django.http import JsonResponse
from django.contrib.auth import logout
from django.contrib.auth.hashers import make_password ,check_password
import datetime
from django.http import HttpResponse
from django.template.loader import render_to_string


def generate_html_view(request):
    if request.method == 'POST':
        # 1. Gather data from the form POST request
        title = request.POST.get('title', 'Untitled Topic')
        summary = request.POST.get('summary', 'No summary.')
        purpose = request.POST.get('purpose', 'No purpose.')
        topic_list=Topic.objects.all()

        # 2. Context for rendering the download template
        context = {
            'title': title,
            'summary': summary,
            'purpose': purpose,

            # Add any other data your complex template needs (e.g., logo URLs)
        }

        # 3. Render the full HTML content from the dedicated template
        html_content = render_to_string('generated_topic.html', context)

        # 4. Create the file name and the HTTP response
        filename = f"{title.replace(' ', '_')}_{datetime.date.today()}.html"

        response = HttpResponse(html_content, content_type='text/html')

        # 5. Set the header to force the browser to download the file
        response['Content-Disposition'] = f'attachment; filename="{filename}"'

        return response

    # If accessed by GET or anything else, redirect or return error
    return redirect('admin_page')

################################--Admin related views-- ##########################################
def create_topic_view(request):
    """Handles creating a new topic from the Add Topic modal form submission."""
    try:
        # Get data 
        title = request.POST.get('title')
        summary = request.POST.get('summary')
        purpose = request.POST.get('purpose')
        
        #text = request.POST.get('text', '') 

        
        if not title:
            return redirect('admin_page') 

        # Create and save the new Topic object
        Topic.objects.create(
            title=title,
            summary=summary,
            purpose=purpose,
            #text=text
        )

        # Redirect back to the main topics list page 
        return redirect('admin_page') 

    except Exception as e:
        print(f"Error during topic creation: {e}")
        # Redirect back to the list page on failure
        return redirect('admin_page')


# ---  View to Handle Topic Deletion ---

def update_topic_view(request, pk):
    """Handles updating an existing topic from the Edit Topic modal form submission."""
    try:
        # Get the existing topic object
        topic = get_object_or_404(Topic, topic_id=pk)

        # Get data from request.POST
        topic.title = request.POST.get('title', topic.title)
        topic.summary = request.POST.get('summary', topic.summary)
        topic.purpose = request.POST.get('purpose', topic.purpose)
       # topic.text = request.POST.get('text', topic.text)

        
        if not topic.title:
            # Handle error: title cannot be empty
            messages.error(request, "Error: The Topic Title cannot be empty. Please fill in the required field.")
            return redirect('admin_page')

        # Save changes to the database
        topic.save()

        return redirect('admin_page')

    except Exception as e:
        import traceback
        # Print the full error stack to the terminal for debugging
        traceback.print_exc() 
        print(f"Error during topic operation (ID: {pk} if applicable): {e}")
        print(f"POST Data Received: {request.POST}")
        
        return redirect('admin_page')


def delete_topic_view(request, pk):
    """Handles deleting a topic via standard POST form submission (from hidden form)."""
    try:
        # Get the Topic object using the primary key (pk)
        topic = get_object_or_404(Topic, topic_id=pk)
        topic.delete()
        
        return redirect('admin_page')
    
    except Exception as e:
        print(f"Error during topic deletion (ID: {pk}): {e}")
        return redirect('admin_page')
    
def adminlogin_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            admin = Admins.objects.get(email=email)
            if  check_password(password , admin.admin_password):  
                full_name = f"{admin.first_name} {admin.last_name}"
                request.session['full_name'] = f"{admin.first_name} {admin.last_name}"
                request.session['email'] = admin.email
                messages.success(request, "Login successful!")
                return render(request, 'admin_page.html', {'full_name': full_name ,'email': email})
                #messages.success(request, "Login successful!")
                 
            else:
                messages.error(request, "Invalid password.")
        except Admins.DoesNotExist:
            messages.error(request, "Email not registered.")

    return render(request, 'adminlogin.html')

#########
def delete_account_view(request):
    email_from_session = request.session.get('email')
    
    if request.method == "POST":
        try:
            admin = Admins.objects.get(email=email_from_session)
            admin.delete()    # Delete the admin from the database
            
            logout(request)   # Log out admin
            
            messages.success(request, "Your account has been deleted successfully.")
            return redirect('adminlogin')   # Redirect to the login page after deletion
            
        except Admins.DoesNotExist:
            messages.error(request, "User does not exist or has already been deleted.")
            return redirect('adminlogin')

    # render confirmation if accessed with GET
    return render(request, 'confirm_delete.html')  

###########
  
def setting_view(request):
    email_from_session = request.session.get('email')
    
    try:
        admin = Admins.objects.get(email=email_from_session)
    except Admins.DoesNotExist:
        messages.error(request, "User does not exist.")
        return redirect('adminlogin')  

    if request.method == "POST":
        # Get the data from the form
        name = request.POST.get('name')
        email = request.POST.get('email')

        # Handle the update of admin's information
        try:
            # Update admin's attributes
            admin.first_name, admin.last_name = name.split(" ")  # Split the name
            admin.email = email  # Update the email
            
            # Save the changes to the database
            admin.save()

            # Update session values to reflect changes
            request.session['full_name'] = name
            request.session['email'] = email

            messages.success(request, "Profile updated successfully!")
            return redirect('setting')  # Redirect to settings page after updating
            
        except Exception as e:
            messages.error(request, f"An error occurred while updating the profile: {str(e)}")
            return redirect('setting')

    # Populate initial values for rendering the form
    full_name = f"{admin.first_name} {admin.last_name}"
    email = admin.email
  
    context = {
        'full_name': full_name,
        'email': email,
    }

    return render(request, 'setting.html', context)

####################

def get_full_name(request):
    """ function to get the full name of the authenticated admin."""
    if request.user.is_authenticated:
        try:
            admin = Admins.objects.get(email=request.user.email)
            return f"{admin.first_name} {admin.last_name}"
        except Admins.DoesNotExist:
            return ''  # Return an empty string if not found
    return ''  
######################3

def extract_student_info(search_term=None):
    """Retrieves Students records from the database"""
   
    student_queryset = Students.objects.all() 

    
    if search_term:
        # Filter for the term being present 
        student_queryset = student_queryset.filter(
            Q(first_name__icontains=search_term) |
            Q(last_name__icontains=search_term) |
            Q(email__icontains=search_term)
        )
    
    student_queryset = student_queryset.order_by('last_name', 'first_name')
        
    std_list = []

    # Loop through the filtered QuerySet
    for user in student_queryset:
        
        # Combine names into full name
        full_name = f"{user.first_name} {user.last_name}".strip()
        
        student_data = {
            "id": user.student_id, 
            "full_name": full_name,
            "email": user.email,
        }
        std_list.append(student_data)

    return std_list

def users_view(request):
    """
     view to display the users table.
    """
    #  Retrieve the search query from the URL parameters (GET request)
    search_term = request.GET.get('search', '').strip()
    
    # Fetch student data
    std_list = extract_student_info(search_term=search_term)
    
    # Retrieve session data (for Admin info display)
    session_full_name = request.session.get('full_name', 'Admin User') 
    
    # 4. Build the context dictionary
    context = {
        'full_name': session_full_name,
        'student_records': std_list, 
        'search_term': search_term, 
    }
    
    # 5. Render the template
    return render(request, 'users.html', context)

from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods



@require_http_methods(["POST"])
def delete_student_view(request, pk):
    """Handles deleting a student """
    try:
        # Get the student object or return a 404 error
        student = get_object_or_404(Students, student_id=pk)
        
        # Perform the deletion
        student.delete()
        
        # Redirect back to the user list page upon successful deletion
        return redirect('users') 
    
    except Exception as e:
        print(f"Error during student deletion (ID: {pk}): {e}")
        return redirect('users')

# --- UPDATE FUNCTION ---


def update_student_view(request, pk):
    """Handles updating student name/email via standard POST form submission."""
    try:
        # Retrieve data from the standard form submission dictionary (request.POST)
        new_full_name = request.POST.get('full_name')
        new_email = request.POST.get('email')
        
        student = get_object_or_404(Students, student_id=pk)

        # --- Handle Full Name Split  ---
        if not new_full_name or not new_email:
            return redirect('users') 

        name_parts = new_full_name.split(' ', 1)
        new_first_name = name_parts[0]
        new_last_name = name_parts[1] if len(name_parts) > 1 else "" 
        
        #  Update the model instance fields
        student.first_name = new_first_name
        student.last_name = new_last_name
        student.email = new_email
        
        #  Save changes to the database
        student.save()

        # Redirect back to the main users list after success 
        return redirect('users')

    except Exception as e:
        print(f"Error during student update (ID: {pk}): {e}")
        return redirect('users')
    
#######################

def admin_view(request):
    full_name = request.session.get('full_name', '') 
    email = request.session.get('email', '') 
    topics_list = Topic.objects.all()
    search_term = request.GET.get('search', '').strip()
    if search_term:
        topics_list = topics_list.filter(
            Q(title__icontains=search_term) |
            Q(summary__icontains=search_term) 
        ).distinct()

    print(f"Number of topics retrieved: {topics_list.count()}")
    context = {
        'full_name': full_name,
        'email': email,
        'topics_list': topics_list ,
        'search_term': search_term,
    }
    return render(request, 'admin_page.html', context)

##############################--User Views--#######################3

def user_homepage_view(request):
    full_name = request.session.get('full_name', '')  
    email = request.session.get('email', '')
    topics_list = Topic.objects.all()
    context = {
        'full_name': full_name,
        'email': email,
        'topic_list':topics_list
    }
    return render(request, 'user_greeting_page.html', context)

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



def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)

        if form.is_valid():
            # Create an instance of the student and hash the password
            student = Students(
                student_password= make_password(form.cleaned_data['password']),  
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                email=form.cleaned_data['email']
            )
            student.save()

            messages.success(request, "Account created successfully.")
            return redirect('login')  # Redirect to the login page 

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




def login_view(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = Students.objects.get(email=email)
            if check_password(password, user.student_password)  :  # Verify password
                # Store the full name in the session
                request.session['full_name'] = f"{user.first_name} {user.last_name}"  
                request.session['email'] = user.email
                return redirect('user_homepage')  # Redirect to user homepage
            else:
                messages.error(request, "Invalid password.")
        except Students.DoesNotExist:
            messages.error(request, "User does not exist.")
    
    return render(request, 'login.html')  # Render the login template






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




def user_page_view(request):
    full_name = request.session.get('full_name', '')  
    email = request.session.get('email', '')
    user = request.user 
    student_id = request.session.get('student_id')  

    # Fetch data from the database
    saved_topics = Save.objects.filter(student=student_id)  
    notes = Note.objects.filter(student=student_id)
    liked_content = Like.objects.filter(student=student_id)

    # context with full name and content
    context = {
        'full_name': full_name,
        'saved_topics': saved_topics,
        'notes': notes,
        'liked_content': liked_content,
        'email' : email,
    }
    
    return render(request, 'user_page.html', context)




















def topic_detail_view(request, topic_id):
    
    topic = get_object_or_404(Topic, topic_id=topic_id)
    
    context = {
        
        'topic_detail': topic 
    }
    
    return render(request, 'generated_topic.html', context)

