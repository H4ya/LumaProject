from .models import Admins
from django.contrib.auth.decorators import login_required

from .models import Admins

def admin_full_name(request):
    if request.user.is_authenticated:
        try:
            admin = Admins.objects.get(email=request.user.email)
            return {'full_name': f"{admin.first_name} {admin.last_name}"}
        except Admins.DoesNotExist:
            return {'full_name': ''}  # Return an empty string if admin doesn't exist
    return {'full_name': ''}  