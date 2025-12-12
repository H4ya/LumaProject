from django.shortcuts import render, redirect , get_object_or_404
from django.contrib import messages
from django.db.models import Q
from .models import *
from .forms import SignupForm
from django.contrib.auth import logout
from django.contrib.auth.hashers import make_password ,check_password
from django.db import transaction
from django.http import JsonResponse, HttpResponseBadRequest
from django.db import IntegrityError
from django.urls import reverse


#**************########################3---------------------Main views ----------------#########################********************


def topic_detail_view(request, topic_id):
    student_id = request.session.get('student_id')
    topic = get_object_or_404(
        Topic.objects.prefetch_related(
            'real_world_magic_points',
            'learning_unlocks',
            'external_resources'
        ), 
        topic_id=topic_id
    )
    
    context = {
        'topic_detail': topic, 
        'magic_points': topic.real_world_magic_points.all(),
        'unlocks': topic.learning_unlocks.all(),
        'resources': topic.external_resources.all(),
        'student_id':student_id
    }
    
    return render(request, 'generated_topic.html', context)

def homepage_view(request):
    topic = Topic.objects.all()
    context={
        'topic':topic
    }
    return render(request, 'homepage.html',context)

def about_view(request):
    return render(request, 'about.html')

def role_view(request):
    return render(request, 'role.html') 


################################--Admin related views-- ##########################################

# admin login view

def adminlogin_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        password = request.POST.get('password')

        try:
            admin = Admins.objects.get(email=email)
            if  check_password(password , admin.admin_password):  
                full_name = f"{admin.first_name} {admin.last_name}"
                request.session['full_name'] = f"{admin.first_name} {admin.last_name}"
                request.session['email'] = admin.email
                request.session['admin_id'] = admin.admin_id
                messages.success(request, "Login successful!")
                return render(request, 'setting.html', {'full_name': full_name ,'email': email})
                 
            else:
                messages.error(request, "Invalid password.")
        except Admins.DoesNotExist:
            messages.error(request, "Email not registered.")

    return render(request, 'adminlogin.html')



def admin_view(request):
    full_name = request.session.get('full_name', '') 
    email = request.session.get('email', '') 
    admin_id= request.session.get('admin_id', '')
    topics_list = Topic.objects.all()
    search_term = request.GET.get('search', '').strip()
    if search_term:
        topics_list = topics_list.filter(
            Q(title__icontains=search_term) 
        )

    context = {
        'full_name': full_name,
        'email': email,
        'topics_list': topics_list ,
        'search_term': search_term,
        'admin_id':admin_id
    }
    return render(request, 'admin_page.html', context)

# admin settengs account view


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

# admin delete account view

def delete_account_view(request):
    email_from_session = request.session.get('email')
    
    if request.method == "POST":
        try:
            admin = Admins.objects.get(email=email_from_session)
            admin.delete()    # Delete the admin from the database
            
            logout(request)   # Log out admin
            return redirect('adminlogin')   # Redirect to the login page after deletion
            
        except Admins.DoesNotExist:
            return redirect('adminlogin')

    # render confirmation if accessed with GET
    return render(request, 'confirm_delete.html')  



################################--Admin control views-- ##########################################



# admin add topic view (rendering to the template)

def add_topic_view (request):
    full_name = request.session.get('full_name', 'Admin') 
    
    context = {
        'full_name': full_name,
    }
    
    # Renders the template file named 'add_topic.html'
    return render(request, 'add_topic.html', context)

# admin add topic view

def create_topic_view(request):
    
    if request.method == 'POST':
        admin_id = request.session.get('admin_id') 
        if not admin_id:
            return HttpResponseBadRequest("Admin session required to create topic.")
        try:
            # Fetch the Admins object instance using the ID
            admin_obj = Admins.objects.get(admin_id=admin_id)
        except Admins.DoesNotExist:
            # This handles cases where the ID exists in the session but not the DB
            return HttpResponseBadRequest("Admin user not found for the current session.")
        
        # ---  Start Atomic Transaction (All or Nothing) ---
        try:
            with transaction.atomic():
                # Save Main Topic (Topics Table)
                new_topic = Topic.objects.create(
                    title=request.POST.get('title'),
                    subtitle=request.POST.get('subtitle'),
                    purpose=request.POST.get('purpose'),
                    why_it_matters=request.POST.get('why_it_matters'),
                    mini_story=request.POST.get('mini_story'),
                    icon = request.POST.get('icon'),
                    status = request.POST.get('status') ,
                   admin=admin_obj
                )

                #  Save Real-World Magic (Real_World_Magic Table)
                for i in range(1, 4): 
                    icon = request.POST.get(f'magic_icon_{i}')
                    title = request.POST.get(f'magic_title_{i}')
                    desc = request.POST.get(f'magic_desc_{i}')
                    
                    if title: # Only save if a title exists
                        RealWorldMagic.objects.create(
                            topic=new_topic,
                            icon=icon,
                            card_title=title,
                            card_description=desc
                        )

                #  Save Learning Unlocks (Learning_Unlocks Table)
                for i in range(1, 4):
                    item_text = request.POST.get(f'unlock_item_{i}')
                    
                    if item_text: # Only save if text exists
                        LearningUnlock.objects.create(
                            topic=new_topic,
                            list_item=item_text
                        )

                #  Save External Resources (External_Resources Table)
                for i in range(1, 4): 
                    icon = request.POST.get(f'resource_icon_{i}')
                    title = request.POST.get(f'resource_title_{i}')
                    url = request.POST.get(f'resource_url_{i}')
                    
                    if title and url: # Only save if title AND URL exist
                        ExternalResource.objects.create(
                            topic=new_topic,
                            icon=icon,
                            link_title=title,
                            url=url
                        )
            
            # --- Redirect on Success ---
            return redirect('admin_page') 

        except Exception as e:
            # Handle any exceptions during save, log it, and return to form with an error message
            print(f"Error saving topic: {e}")
            # Rerender the form with an error message 
            return render(request, 'add_topic.html', {
                'error_message': 'Failed to save topic. Check inputs and server logs.'
            })

    # Render the empty form on GET request
    return render(request, 'add_topic.html')

# Edit topic view 

def edit_topic_view(request, topic_id):
    full_name = request.session.get('full_name', '')
    topic = get_object_or_404(
        Topic.objects.prefetch_related(
            'real_world_magic_points',
            'learning_unlocks',
            'external_resources'
        ), 
        topic_id=topic_id
    )
    
    
    context = {
        'full_name':full_name,
        'topic': topic, 
        'magic_points': topic.real_world_magic_points.all(),
        'unlocks': topic.learning_unlocks.all(),
        'resources': topic.external_resources.all(),
    }
    
    # Render the dedicated edit form template
    return render(request, 'edit_topic.html', context)


#  View to Handle Topic Deletion and Update 

def update_topic_view(request, topic_id):
    
    if request.method == 'POST':
        admin_id = request.session.get('admin_id') 
        
        #  Authentication Check & Topic Retrieval
        if not admin_id:
            messages.error(request, "Authentication failed. Admin session required.")
            return redirect('admin_page')
        
        topic_to_update = get_object_or_404(Topic, topic_id=topic_id)
        
        try:
            with transaction.atomic():
                #  Update Main Topic Fields
                topic_to_update.title = request.POST.get('title')
                topic_to_update.subtitle = request.POST.get('subtitle')
                topic_to_update.purpose = request.POST.get('purpose')
                topic_to_update.why_it_matters = request.POST.get('why_it_matters')
                topic_to_update.mini_story = request.POST.get('mini_story')
                topic_to_update.icon = request.POST.get('icon')
                topic_to_update.status = request.POST.get('status')
                topic_to_update.save() 

                # Update/Delete/Create Related Tables ( Magic, Unlocks, Resources)
                for i in range(1, 4):
                    magic_id = request.POST.get(f'magic_id_{i}')
                    title = request.POST.get(f'magic_title_{i}')
                    
                    if magic_id: 
                        magic_obj = RealWorldMagic.objects.get(magic_id=magic_id)
                        if title: 
                            magic_obj.icon = request.POST.get(f'magic_icon_{i}')
                            magic_obj.card_title = title
                            magic_obj.card_description = request.POST.get(f'magic_desc_{i}')
                            magic_obj.save()
                        else: 
                            magic_obj.delete()
                    elif title: 
                        RealWorldMagic.objects.create(
                            topic=topic_to_update,
                            icon=request.POST.get(f'magic_icon_{i}'),
                            card_title=title,
                            card_description=request.POST.get(f'magic_desc_{i}')
                        )
                
                for i in range(1, 4):
                    unlock_id = request.POST.get(f'unlock_id_{i}')
                    item_text = request.POST.get(f'unlock_item_{i}')
                    
                    if unlock_id: 
                        unlock_obj = LearningUnlock.objects.get(unlock_id=unlock_id)
                        if item_text:
                            unlock_obj.list_item = item_text
                            unlock_obj.save()
                        else:
                            unlock_obj.delete()
                    elif item_text: 
                        LearningUnlock.objects.create(
                            topic=topic_to_update,
                            list_item=item_text
                        )
                        
                for i in range(1, 4):
                    resource_id = request.POST.get(f'resource_id_{i}')
                    title = request.POST.get(f'resource_title_{i}')
                    url = request.POST.get(f'resource_url_{i}')
                    
                    if resource_id:
                        resource_obj = ExternalResource.objects.get(resource_id=resource_id)
                        if title and url:
                            resource_obj.icon = request.POST.get(f'resource_icon_{i}')
                            resource_obj.link_title = title
                            resource_obj.url = url
                            resource_obj.save()
                        else:
                            resource_obj.delete()
                    elif title and url:
                        ExternalResource.objects.create(
                            topic=topic_to_update,
                            icon=request.POST.get(f'resource_icon_{i}'),
                            link_title=title,
                            url=url
                        )

            #  Success: Set the message and redirect to the admin page
            messages.success(request, f"Topic '{topic_to_update.title}' successfully updated!")
            return redirect('admin_page') 

        except Exception as e:
            # Failure: Set the error message and redirect back to the edit page
            messages.error(request, f"Failed to save topic changes: {str(e)}")
            return redirect('edit_topic', topic_id=topic_id)
    
    # Redirect the user back to the admin list page for non-POST methods.
    messages.error(request, "Invalid request method used for update.")
    return redirect('admin_page')



def delete_topic_view(request, pk):
    try:
        # Get the Topic object using the primary key (pk)
        topic = get_object_or_404(Topic, topic_id=pk)
        topic.delete()
        
        return redirect('admin_page')
    
    except Exception as e:
        print(f"Error during topic deletion (ID: {pk}): {e}")
        return redirect('admin_page')

###########    


# Handel the Extracting of Student in the database


def extract_student_info(search_term=None):
    # Retrieves Students records from the database
   
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


# view to display the users table.

def users_view(request):
    search_term = request.GET.get('search', '').strip()
    # Fetch student data
    std_list = extract_student_info(search_term=search_term)
    
    # Retrieve session data (for Admin info display)
    session_full_name = request.session.get('full_name', 'Admin User') 
    context = {
        'full_name': session_full_name,
        'student_records': std_list, 
        'search_term': search_term, 
    }
    
    #  Render the template
    return render(request, 'users.html', context)

# Handles deleting a student

def delete_student_view(request, pk):
     
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
    

# Handles updating student name/email via standard POST form submission

def update_student_view(request, pk):
    
    try:
        # Retrieve data 
        new_full_name = request.POST.get('full_name')
        new_email = request.POST.get('email')
        
        student = get_object_or_404(Students, student_id=pk)

        # Handle Full Name Split 
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



##############################--User Views--#######################

# signup view

def signup_view(request):
    # Handle the form submission (POST request)
    if request.method == 'POST':
        form = SignupForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data['email']
            
            if Students.objects.filter(email)==email:
                messages.error(request, "The email address is already registered. Please log in.")
                return redirect('signup') # Redirect back to the signup page to show the error
            
            try:
                # Create the instance
                student = Students(
                    student_password=make_password(form.cleaned_data['password']), 
                    first_name=form.cleaned_data['first_name'],
                    last_name=form.cleaned_data['last_name'],
                    email=email
                )
                student.save()
                
                # SUCCESS RESPONSE 
                messages.success(request, 'Account created successfully! Please log in.')
                return redirect('signup') 

            except IntegrityError:
                messages.error(request, "A database error occurred. Could not complete registration.")
                return redirect('signup')

        else:
        
            messages.error(request, 'Registration failed. Please check your details.')
            return render(request, 'signup.html', {'form': form}) 

    # Handle the initial page load 
    else:
        form = SignupForm() 
        return render(request, 'signup.html', {'form': form})






# login view

def login_view(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        student_id = request.session.get('student_id')

        try:
            user = Students.objects.get(email=email)
            if check_password(password, user.student_password)  :  # Verify password
                # Store the full name, email and id in the session
                request.session['full_name'] = f"{user.first_name} {user.last_name}"  
                request.session['email'] = user.email
                request.session['student_id'] = user.student_id
                return redirect('user_homepage')  # Redirect to user homepage
            else:
                messages.error(request, "Invalid password.")
        except Students.DoesNotExist:
            messages.error(request, "User does not exist.")
    
    return render(request, 'login.html')  # Render the login template



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

# Student profile view

def user_page_view(request):
    full_name = request.session.get('full_name', '')  
    email = request.session.get('email', '')
    user = request.user 
    student_id = request.session.get('student_id')  

    saved_topics = Save.objects.filter(std_id=student_id)  
    notes = Note.objects.filter(student=student_id)
    liked_content = Like.objects.filter(std_id=student_id)

    # context with full name and content
    context = {
        'full_name': full_name,
        'saved_topics': saved_topics,
        'notes': notes,
        'liked_content': liked_content,
        'email' : email,
    }
    
    return render(request, 'user_page.html', context)



# API endpoints for fetching user data (JSON)
def get_saved_topics(request):
    student_id = request.session.get('student_id')
    if not student_id:
        return JsonResponse([], safe=False)
    
    saved = Save.objects.filter(std_id=student_id)
    
    data = []
    for save in saved:
        try:
            topic = Topic.objects.get(topic_id=save.topic_id)
            data.append({
                'topic_id': topic.topic_id,
                'title': topic.title,
                'url': reverse('generated_topic', args=[topic.topic_id]),
            })
        except Topic.DoesNotExist:
            continue
    
    return JsonResponse(data, safe=False)


def get_notes(request):
    student_id = request.session.get('student_id')
    if not student_id:
        return JsonResponse([], safe=False)
    
    notes = Note.objects.filter(student=student_id).order_by('-note_id')
    data = [
        {
            'note_id': note.note_id,
            'title': note.topic_title,
            'content': note.note_content,
            'last_edited': note.creation_date.isoformat() + 'Z' if note.creation_date else '',
            'key_takeaway': note.note_content[:200] + '...' if len(note.note_content) > 200 else note.note_content
        }
        for note in notes
    ]
    return JsonResponse(data, safe=False)


def get_likes(request):
    student_id = request.session.get('student_id')
    if not student_id:
        return JsonResponse([], safe=False)
    
    likes = Like.objects.filter(std_id=student_id)
    
    data = []
    for like in likes:
        try:
            topic = Topic.objects.get(topic_id=like.topic_id)
            data.append({
                'topic_id': topic.topic_id,
                'title': topic.title,
                'url': reverse('generated_topic', args=[topic.topic_id]),
            })
        except Topic.DoesNotExist:
            continue
    
    return JsonResponse(data, safe=False)


def toggle_save(request):
    if request.method == 'POST':
        student_id = request.session.get('student_id')
        topic_id = request.POST.get('topic_id')
        
        if not student_id or not topic_id:
            return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)
        
        try:
            # Verify student and topic exist
            student = Students.objects.get(student_id=student_id)
            topic = Topic.objects.get(topic_id=topic_id)
            
            # Use integer fields directly
            save_record = Save.objects.filter(std_id=student_id, topic_id=topic_id).first()
            
            if save_record:
                save_record.delete()
                return JsonResponse({'status': 'removed', 'saved': False})
            else:
                Save.objects.create(std_id=student_id, topic_id=topic_id)
                return JsonResponse({'status': 'added', 'saved': True})
        except (Students.DoesNotExist, Topic.DoesNotExist):
            return JsonResponse({'status': 'error', 'message': 'Student or topic not found'}, status=404)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    
    return JsonResponse({'status': 'error', 'message': 'Invalid method'}, status=405)


def toggle_like(request):
    if request.method == 'POST':
        student_id = request.session.get('student_id')
        topic_id = request.POST.get('topic_id')
        
        if not student_id or not topic_id:
            return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)
        
        try:
            # Verify student and topic exist
            student = Students.objects.get(student_id=student_id)
            topic = Topic.objects.get(topic_id=topic_id)
            
            # Use integer fields directly
            like_record = Like.objects.filter(std_id=student_id, topic_id=topic_id).first()
            
            if like_record:
                like_record.delete()
                return JsonResponse({'status': 'removed', 'liked': False})
            else:
                Like.objects.create(std_id=student_id, topic_id=topic_id)
                return JsonResponse({'status': 'added', 'liked': True})
        except (Students.DoesNotExist, Topic.DoesNotExist):
            return JsonResponse({'status': 'error', 'message': 'Student or topic not found'}, status=404)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    
    return JsonResponse({'status': 'error', 'message': 'Invalid method'}, status=405)




def save_note(request):
    if request.method == 'POST':
        student_id = request.session.get('student_id')
        topic_id = request.POST.get('topic_id')
        note_content = request.POST.get('note_content')
        topic_title = request.POST.get('topic_title', 'Untitled')
        
        if not student_id:
            return JsonResponse({'status': 'error', 'message': 'Please log in to save notes'}, status=401)
        
        if not note_content or not note_content.strip():
            return JsonResponse({'status': 'error', 'message': 'Note content cannot be empty'}, status=400)
        
        try:
            student = Students.objects.get(student_id=student_id)
            
            
            Note.objects.create(
                student=student,
                topic_title=topic_title,
                note_content=note_content,
                
            )
            
            return JsonResponse({'status': 'success', 'message': 'Note saved successfully!'})
        except Students.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Student not found'}, status=404)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': f'Error saving note: {str(e)}'}, status=500)
    
    return JsonResponse({'status': 'error', 'message': 'Invalid method'}, status=405)


def delete_note(request):
    if request.method == 'POST':
        student_id = request.session.get('student_id')
        note_id = request.POST.get('note_id')
        
        if not student_id:
            return JsonResponse({'status': 'error', 'message': 'Please log in'}, status=401)
        
        if not note_id:
            return JsonResponse({'status': 'error', 'message': 'Note ID required'}, status=400)
        
        try:
            note = Note.objects.get(note_id=note_id, student__student_id=student_id)
            note.delete()
            return JsonResponse({'status': 'success', 'message': 'Note deleted successfully!'})
        except Note.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Note not found'}, status=404)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': f'Error deleting note: {str(e)}'}, status=500)
    
    return JsonResponse({'status': 'error', 'message': 'Invalid method'}, status=405)


def update_note(request):
    if request.method == 'POST':
        student_id = request.session.get('student_id')
        note_id = request.POST.get('note_id')
        note_content = request.POST.get('note_content')
        
        if not student_id:
            return JsonResponse({'status': 'error', 'message': 'Please log in'}, status=401)
        
        if not note_id or not note_content:
            return JsonResponse({'status': 'error', 'message': 'Note ID and content required'}, status=400)
        
        try:
            note = Note.objects.get(note_id=note_id, student__student_id=student_id)
            note.note_content = note_content
            note.save()
            return JsonResponse({'status': 'success', 'message': 'Note updated successfully!'})
        except Note.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Note not found'}, status=404)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': f'Error updating note: {str(e)}'}, status=500)
    
    return JsonResponse({'status': 'error', 'message': 'Invalid method'}, status=405)



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