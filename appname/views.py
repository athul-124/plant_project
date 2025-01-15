# views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.models import User
import json
from .forms import SpaceImageForm
from django.core.paginator import Paginator
from django.http import JsonResponse



import random
from .models import Plant

def home(request):
    return render(request, 'home.html')

# Register View
def register(request):
    if request.method == 'POST':
        # Use .get() to avoid MultiValueDictKeyError
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm-password')
        phone = request.POST.get('phone')
        address = request.POST.get('address')

        # Check if all fields are provided
        if not all([name, email, password, confirm_password, phone, address]):
            messages.error(request, "All fields are required!")
            return render(request, 'register.html')

        # Check if passwords match
        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return render(request, 'register.html')

        try:
            # Create the user
            user = User.objects.create_user(username=email, email=email, password=password)
            user.first_name = name
            user.save()

            # Optionally, create a profile or save extra fields
            # user.profile.phone = phone
            # user.profile.address = address
            # user.profile.save()

            messages.success(request, "Registration successful! You can now log in.")
            return redirect('login')  # Redirect to the login page

        except Exception as e:
            messages.error(request, f"Error: {e}")
            return render(request, 'register.html')

    return render(request, 'register.html')


# Login View
def login_view(request):  # Renamed function to avoid confusion with Django's `login` method
    if request.method == 'POST':
        # Retrieve 'username' and 'password' from the POST data
        username = request.POST.get('username')  # use .get() to avoid errors if field is missing
        password = request.POST.get('password')
        
        if username and password:
            # Authenticate the user
            user = authenticate(request, username=username, password=password)

            if user is not None:
                # If authentication is successful, log the user in
                login(request, user)  # Correct function name to log in the user
                messages.success(request, "Login successful!")
                return redirect('home')  # Redirect to the home page or any other page after login
            else:
                # If authentication fails
                messages.error(request, "Invalid username or password.")
                return render(request, 'login.html')
        else:
            # If username or password is missing
            messages.error(request, "Both username and password are required.")
            return render(request, 'login.html')

    return render(request, 'login.html')


from django.shortcuts import render
from django.http import JsonResponse
from appname.models import Plant  # Import your Plant model

def chatbot_page(request):
    return render(request, 'appname/chat.html')

def chatbot_response(request):
    if request.method == "POST":
        message = json.loads(request.body).get('message')

        if message:
            # Query the database for plant details
            plant = Plant.objects.filter(common_name__icontains=message).first()

            if plant:
                # If plant is found, return its details
                response_data = {
                    'common_name': plant.common_name,
                    'family': plant.family,
                    'categories': plant.categories,
                    'origin': plant.origin,
                    'climate': plant.climate,
                    'zone': plant.zone,
                    'img_url': plant.img_url,
                }
                return JsonResponse(response_data)
            else:
                # If no plant is found
                return JsonResponse({'message': "Sorry, I couldn't find any information about that plant."})
        return JsonResponse({'message': "Please ask a valid question."})
    return JsonResponse({'message': "Invalid request method"})


def upload_image(request):
    if request.method == 'POST':
        form = SpaceImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('upload_image')  # Redirect back to the upload page after uploading
    else:
        form = SpaceImageForm()

    return render(request, 'upload_image.html', {'form': form})

def plant_library(request):
    plants = Plant.objects.all()  # Fetch all rows from the plants table
    paginator = Paginator(plants, 20)  # Show 20 plants per page
    page_number = request.GET.get('page')  # Get the page number from the URL
    page_obj = paginator.get_page(page_number)  # Get the plants for the current page
    return render(request, 'plant_library.html', {'page_obj': page_obj})







PLANT_DATABASE = [
    {"name": "Snake Plant", "light": "low", "humidity": "low", "type": "foliage"},
    {"name": "Peace Lily", "light": "low", "humidity": "high", "type": "flowering"},
    {"name": "Aloe Vera", "light": "high", "humidity": "low", "type": "succulent"},
    {"name": "Fern", "light": "medium", "humidity": "high", "type": "foliage"},
    {"name": "Cactus", "light": "high", "humidity": "low", "type": "succulent"},
    {"name": "Orchid", "light": "medium", "humidity": "high", "type": "flowering"},
]

# Process AJAX request to find plants
def plant_advisor(request):
    if request.method == "POST":
        light = request.POST.get('light')
        humidity = request.POST.get('humidity')
        plant_type = request.POST.get('type')

        # Filter plants based on user input
        plants = Plant.objects.filter(
            categories__icontains=plant_type,
            climate__icontains=humidity,
            origin__icontains=light
        )
        plant_list = [
            {
                "common_name": plant.common_name,
                "family": plant.family,
                "image_url": plant.image_url
            }
            for plant in plants
        ]
        return JsonResponse({"plants": plant_list})

    return render(request, "plant_advisor.html")
                             


from .models import Expert

def expert_advice(request):
    experts = Expert.objects.all()  # Fetch all experts from the database
    return render(request, 'expert_advice.html', {'experts': experts})


from .forms import PlantAdvisorForm
from .models import PlantInfo  # Use the new model name

def plant_advisor(request):
    if request.method == 'POST':
        form = PlantAdvisorForm(request.POST)
        if form.is_valid():
            # Get form data
            light_level = form.cleaned_data['light_level']
            humidity = form.cleaned_data['humidity']
            plant_type = form.cleaned_data['plant_type']
            watering_frequency = form.cleaned_data['watering_frequency']
            soil_type = form.cleaned_data['soil_type']

            # Query the PlantInfo model based on user input
            plants = PlantInfo.objects.filter(
                light_level=light_level,
                humidity=humidity,
                plant_type__icontains=plant_type,
                watering_frequency=watering_frequency,
                soil_type=soil_type
            )
            
            return render(request, 'appname/plant_advisor_results.html', {'plants': plants})
    else:
        form = PlantAdvisorForm()

    return render(request, 'appname/plant_advisor.html', {'form': form})


def care(request):
    return render(request, 'care.html')