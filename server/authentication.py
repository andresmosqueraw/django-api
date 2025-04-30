from rest_framework.authentication import TokenAuthentication

class MultiTokenAuthentication(TokenAuthentication):
    def authenticate(self, request):
        auth = request.headers.get('Authorization', '').split()

        if not auth or auth[0].lower() not in ['token', 'bearer']:
            return None

        if len(auth) == 1:
            return None  # Token sin valor
        elif len(auth) > 2:
            return None  # Token con espacios

        return self.authenticate_credentials(auth[1])