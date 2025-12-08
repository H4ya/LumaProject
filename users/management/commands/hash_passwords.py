from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from django.db import transaction

try:
    # Importing both models 
    from users.models import Students, Admins 
except ImportError:
    # Fallback/placeholder if the model is not found, adjust this line!
    # Define dummy classes for both models to prevent crashes if the real models aren't imported
    class Students:
        @staticmethod
        def objects(): return [] 
    class Admins:
        @staticmethod
        def objects(): return [] 
    
class Command(BaseCommand):
    """
    Hashes plain-text passwords for existing students and admins in the database.
    This is a one-time migration command.
    """
    help = 'Hashes unhashed passwords for existing Student and Admin records.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING('Starting password hashing migration for Students and Admins...'))
        
        total_updated = 0
        
        # We wrap the operation in a transaction for safety
        with transaction.atomic():
            
            # =================================================================
            # 1. Processing Students Table
            # =================================================================
            self.stdout.write(self.style.WARNING('\nProcessing Students records...'))
            students_to_update = Students.objects.all()

            for student in students_to_update:
                # Check if the password is ALREADY hashed
                if student.student_password and student.student_password.startswith(('pbkdf2', 'sha1', 'bcrypt')):
                    self.stdout.write(self.style.NOTICE(f'Skipping Student ID {student.student_id} - Password appears to be already hashed.'))
                    continue
                
                # Assume the password is plain text and hash it
                if student.student_password:
                    hashed_password = make_password(student.student_password)
                    
                    # Update the student record
                    student.student_password = hashed_password
                    student.save(update_fields=['student_password'])
                    total_updated += 1
                    
                    self.stdout.write(self.style.SUCCESS(f'Successfully hashed password for Student ID {student.student_id} ({student.email})'))

            # =================================================================
            # 2. Processing Admins Table
            # =================================================================
            self.stdout.write(self.style.WARNING('\nProcessing Admins records...'))
            admins_to_update = Admins.objects.all()

            
            PASSWORD_FIELD_ADMIN = 'admin_password' 

            for admin in admins_to_update:
                admin_password = getattr(admin, PASSWORD_FIELD_ADMIN)
                
                # Check if the password is ALREADY hashed
                if admin_password and admin_password.startswith(('pbkdf2', 'sha1', 'bcrypt')):
                    self.stdout.write(self.style.NOTICE(f'Skipping Admin ID {admin.admin_id} - Password appears to be already hashed.'))
                    continue
                
                # Assume the password is plain text and hash it
                if admin_password:
                    hashed_password = make_password(admin_password)
                    
                    # Update the admin record
                    setattr(admin, PASSWORD_FIELD_ADMIN, hashed_password)
                    admin.save(update_fields=[PASSWORD_FIELD_ADMIN])
                    total_updated += 1
                    
                    # Assuming Admins also have an email field for logging
                    self.stdout.write(self.style.SUCCESS(f'Successfully hashed password for Admin ID {admin.admin_id} ({admin.email})'))

            if total_updated > 0:
                self.stdout.write(self.style.SUCCESS(f'\nPassword hashing complete. Total {total_updated} records updated across Students and Admins.'))
            else:
                self.stdout.write(self.style.WARNING('\nNo plain-text passwords found that needed updating.'))