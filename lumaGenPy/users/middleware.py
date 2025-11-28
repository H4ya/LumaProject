from .models import Admins
from django.utils.deprecation import MiddlewareMixin

class AdminFullNameMiddleware(MiddlewareMixin):
    def process_template_response(self, request, response):
        if request.user.is_authenticated:
            try:
                admin = Admins.objects.get(email=request.user.email)
                response.context_data['full_name'] = f"{admin.first_name} {admin.last_name}"
            except Admins.DoesNotExist:
                response.context_data['full_name'] = None
        return response