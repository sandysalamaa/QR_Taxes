from rest_framework import authentication
from firebase_admin import auth
from django.contrib.auth import get_user_model
from users.models import User

User = get_user_model()

class FirebaseAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        if not auth_header.startswith('Bearer '):
            return None

        id_token = auth_header.split(' ')[1]
        
        try:
            decoded_token = auth.verify_id_token(id_token)
            firebase_uid = decoded_token['uid']
            email = decoded_token.get('email', '')
            phone = decoded_token.get('phone_number', '')

            # Get or create user
            user, created = User.objects.get_or_create(
                firebase_uid=firebase_uid,
                defaults={
                    'email': email,
                    'phone': phone,
                    'first_name': decoded_token.get('name', '').split()[0] if decoded_token.get('name') else '',
                    'last_name': ' '.join(decoded_token.get('name', '').split()[1:]) if decoded_token.get('name') else ''
                }
            )
            
            return (user, None)
            
        except Exception as e:
            return None