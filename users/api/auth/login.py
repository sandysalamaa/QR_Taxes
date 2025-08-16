# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from django.contrib.auth import get_user_model
# import firebase_admin
# from firebase_admin import auth

# User = get_user_model()

# class FirebaseLoginView(APIView):
#     def post(self, request):
#         id_token = request.data.get('id_token')
        
#         try:
#             # Verify Firebase token
#             decoded_token = auth.verify_id_token(id_token)
#             firebase_uid = decoded_token['uid']
            
#             # Get or create user
#             user, created = User.objects.get_or_create(
#                 firebase_uid=firebase_uid,
#                 defaults={
#                     'email': decoded_token.get('email', ''),
#                     'first_name': decoded_token.get('name', '').split()[0] if decoded_token.get('name') else '',
#                     'last_name': ' '.join(decoded_token.get('name', '').split()[1:]) if decoded_token.get('name') else ''
#                 }
#             )
            
#             # Return user data
#             return Response({
#                 'uid': firebase_uid,
#                 'email': user.email,
#                 'first_name': user.first_name,
#                 'last_name': user.last_name,
#                 'is_new_user': created
#             }, status=status.HTTP_200_OK)
            
#         except Exception as e:
#             return Response(
#                 {'error': 'Invalid token or authentication failed'},
#                 status=status.HTTP_401_UNAUTHORIZED
#             )