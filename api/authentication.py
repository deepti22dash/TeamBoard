from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

from .models import Company

class APIKeyAuthentication(BaseAuthentication):

    class APIKeyAuthentication(BaseAuthentication):

        def authenticate(self, request):
            
            api_key = request.headers.get("X-API-Key")

        
            if not api_key:
                return None

            try:
                company = Company.objects.get(api_key=api_key)

            except Company.DoesNotExist:
                raise AuthenticationFailed("Invalid API Key")

            return (company.user, None)