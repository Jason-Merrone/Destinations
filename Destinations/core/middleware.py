from .models import Session
from django.shortcuts import redirect

def session_middleware(get_response):
    def middleware(request):
        session_token = request.COOKIES.get('session_token')
        user = None
        if session_token:
            session = Session.objects.filter(token=session_token).first()
            if session:
                user = session.user
        request.user = user

        # List of paths that don't require authentication
        open_paths = ['/sessions/new', '/users/new', '/']
        
        if not request.user and request.path not in open_paths:
            return redirect('/sessions/new')

        response = get_response(request)
        return response

    return middleware
