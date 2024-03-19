from django.shortcuts import get_object_or_404,render, redirect
from .models import Destination, User, Session
from django.contrib.auth.hashers import make_password, check_password

def index(request):
    # Fetch the 5 most recent publicly shared destinations
    destinations = Destination.objects.filter(share_publicly=True).order_by('-id')[:5]
    return render(request, 'core/index.html', {'destinations': destinations, 'user': request.user})

def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        
        try:
            user = User.objects.get(email=email)
            if check_password(password, user.password_hash):
                # Password is correct, create a session
                session = Session.objects.create(user=user)
                response = redirect('/destinations')
                response.set_cookie('session_token', session.token)
                return response
            else:
                # Password is incorrect
                return render(request, 'core/login.html', {'error': 'Invalid email or password'})
        except User.DoesNotExist:
            # Email does not exist
            return render(request, 'core/login.html', {'error': 'Invalid email or password'})

    return render(request, 'core/login.html',{'user': request.user})

def signup(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        
        # validation
        if not "@" in email:
            return render(request, 'core/signup.html', {'error': 'Enter a valid email address'})
        if len(password) < 8 or not any(char.isdigit() for char in password):
            return render(request, 'core/signup.html', {'error': 'Password must be at least 8 characters long and include a number'})
        
        # Check if user already exists
        if User.objects.filter(email=email).exists():
            return render(request, 'core/signup.html', {'error': 'Email already in use'})
        
        # Create new user
        user = User.objects.create(
            name=name,
            email=email,
            password_hash=make_password(password)
        )
        
        #  log in the user by creating a session
        session = Session.objects.create(user=user)
        response = redirect('/destinations')
        response.set_cookie('session_token', session.token)
        return response

    return render(request, 'core/signup.html', {'user': request.user})

def destinations(request):
    # Ensure the user is logged in
    if not request.user:
        return redirect('/sessions/new')
    
    # Fetch the destinations fo current user
    user_destinations = Destination.objects.filter(user=request.user)
    
    return render(request, 'core/destinations.html', {'destinations': user_destinations, 'user': request.user})

def logout(request):
    session_token = request.COOKIES.get('session_token')
    if session_token:
        # Delete the session from the data base
        Session.objects.filter(token=session_token).delete()
        # Prepare the response and clear the cookie
        response = redirect('/')
        response.delete_cookie('session_token')
        return response
    return redirect('/sessions/new')


def add_destination(request):
    # Ensure  user is logged in
    if not request.user:
        return redirect('/sessions/new')

    if request.method == 'POST':
        name = request.POST['name']
        review = request.POST['review']
        rating = request.POST['rating']
        share_publicly = 'share_publicly' in request.POST

        # Create the new destination
        Destination.objects.create(
            user=request.user,
            name=name,
            review=review,
            rating=rating,
            share_publicly=share_publicly
        )
        return redirect('/destinations')

    return render(request, 'core/add_destination.html', {'user': request.user})

def edit_destination(request, destination_id):
    destination = get_object_or_404(Destination, id=destination_id, user=request.user)

    if request.method == 'POST':
        destination.name = request.POST.get('name', '')
        destination.review = request.POST.get('review', '')
        destination.rating = int(request.POST.get('rating', 1))
        destination.share_publicly = 'share_publicly' in request.POST
        destination.save()
        return redirect('/destinations')

    return render(request, 'core/edit_destination.html', {'destination': destination})

def delete_destination(request, destination_id):
    if request.method == 'POST':
        destination = get_object_or_404(Destination, id=destination_id, user=request.user)
        destination.delete()
        return redirect('/destinations')

    # Redirect to destinations page if not a POST request
    return redirect('/destinations')